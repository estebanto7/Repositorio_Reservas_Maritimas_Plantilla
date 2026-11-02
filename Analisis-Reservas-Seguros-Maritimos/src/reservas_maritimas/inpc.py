"""Actualización monetaria a un periodo mensual del INPC mexicano.

Esta implementación NO descarga índices y NO infiere fechas de emisión reales.
"""
from __future__ import annotations

import re
import pandas as pd


def ajustar_inpc(
    df: pd.DataFrame,
    columnas: str | list[str],
    fecha_col: str,
    fecha_objetivo: str | int,
    inpc: pd.Series,
    frecuencia: str = "anual",
    criterio_anual: str = "diciembre",
) -> pd.DataFrame:
    """Actualiza importes monetarios sin sobrescribir las columnas originales.

    Parameters
    ----------
    df : pandas.DataFrame
        Observaciones con importes y un periodo de origen.
    columnas : str o list[str]
        Columnas monetarias que se ajustarán.
    fecha_col : str
        Columna de origen. Con ``frecuencia='anual'`` admite años como 2024.
    fecha_objetivo : str o int
        Año (se interpreta como diciembre) o periodo `AAAA-MM` de destino.
    inpc : pandas.Series
        Serie de **índices mensuales**, indexada por fechas, con valores > 0.
    frecuencia : {'anual','mensual','diaria'}, default 'anual'
        Interpretación de ``fecha_col``.
    criterio_anual : {'diciembre','promedio'}, default 'diciembre'
        En orígenes anuales, toma diciembre o la media de los 12 meses.

    Returns
    -------
    pandas.DataFrame
        Copia del DataFrame con ``factor_inpc`` y ``{columna}_ajustada``.

    Raises
    ------
    ValueError
        Si hay fechas, índices o montos inválidos o el INPC no cubre los periodos.

    Notes
    -----
    - Ajuste = importe × (INPC destino / INPC origen).
    - Para origen anual se requiere un criterio explícito y defendible.
    - Para fechas diarias se utiliza el índice de su mes.
    - La función no redondea ni imputa periodos ausentes.

    Examples
    --------
    >>> inpc = pd.Series([100, 110], index=pd.to_datetime(['2024-12-01','2025-12-01']))
    >>> base = pd.DataFrame({'año': [2024], 'prima': [1000]})
    >>> ajustar_inpc(base, 'prima', 'año', 2025, inpc)['prima_ajustada'].iloc[0]
    1100.0
    """
    if not isinstance(df, pd.DataFrame) or not isinstance(inpc, pd.Series):
        raise TypeError("df debe ser DataFrame e inpc debe ser Series de pandas.")
    cols = [columnas] if isinstance(columnas, str) else list(columnas)
    if not cols or len(set(cols)) != len(cols):
        raise ValueError("Indica columnas únicas y no vacías.")
    missing = [x for x in [fecha_col, *cols] if x not in df]
    if missing:
        raise KeyError(f"Columnas no encontradas: {missing}")
    if frecuencia not in {"anual", "mensual", "diaria"}:
        raise ValueError("frecuencia debe ser anual, mensual o diaria.")
    if criterio_anual not in {"diciembre", "promedio"}:
        raise ValueError("criterio_anual debe ser diciembre o promedio.")
    targets = [f"{c}_ajustada" for c in cols] + ["factor_inpc"]
    if any(x in df for x in targets):
        raise ValueError("Algunas columnas de salida ya existen en el DataFrame.")

    # Una fecha objetivo que solo tiene año se refiere a diciembre.
    target_text = str(fecha_objetivo).strip()
    if re.fullmatch(r"\d{4}", target_text):
        target_text += "-12"
    target_timestamp = pd.to_datetime(target_text, errors="coerce")
    if pd.isna(target_timestamp):
        raise ValueError("fecha_objetivo inválida.")
    target = target_timestamp.to_period("M")

    if isinstance(inpc.index, pd.PeriodIndex):
        ix = inpc.index.asfreq("M")
    else:
        if pd.api.types.is_numeric_dtype(inpc.index.dtype):
            raise ValueError("Los índices del INPC deben tener fechas, no números.")
        dates = pd.to_datetime(inpc.index, errors="coerce")
        if pd.isna(dates).any():
            raise ValueError("Índice temporal del INPC inválido.")
        ix = dates.to_period("M")
    if ix.has_duplicates:
        raise ValueError("Hay meses repetidos en la serie INPC.")
    values = pd.to_numeric(inpc.to_numpy(), errors="coerce")
    if pd.isna(values).any() or (values <= 0).any():
        raise ValueError("Los valores INPC deben ser positivos y válidos.")
    monthly = pd.Series(values, index=ix).sort_index()
    if target not in monthly:
        raise ValueError(f"No existe INPC para el destino {target}.")

    if frecuencia == "anual":
        raw = df[fecha_col].astype("string").str.strip()
        years = pd.to_numeric(raw, errors="coerce")
        valid_year = raw.str.fullmatch(r"\d{4}(?:\.0+)?").fillna(False)
        if not valid_year.all() or years.isna().any() or not years.between(1000, 9999).all():
            raise ValueError("Para frecuencia anual, fecha_col debe contener años de cuatro cifras.")
        years = years.astype(int)
        if criterio_anual == "diciembre":
            period = pd.PeriodIndex([f"{y}-12" for y in years], freq="M")
            origin = pd.Series(monthly.reindex(period).to_numpy(), index=df.index)
        else:
            n = monthly.groupby(monthly.index.year).size()
            missing_years = sorted({y for y in years if n.get(y, 0) != 12})
            if missing_years:
                raise ValueError(f"Faltan INPC mensuales para calcular promedio anual: {missing_years}")
            annual = monthly.groupby(monthly.index.year).mean()
            origin = pd.Series(years.map(annual).to_numpy(), index=df.index)
    else:
        # Para los periodos mensuales: preferir formatos AAAA-MM o fechas explícitas.
        raw = df[fecha_col].astype("string").str.strip()
        dates = pd.to_datetime(raw, errors="coerce", dayfirst=True, format="mixed")
        if dates.isna().any():
            raise ValueError("Hay fechas de origen inválidas.")
        period = pd.PeriodIndex(dates.dt.to_period("M"), freq="M")
        origin = pd.Series(monthly.reindex(period).to_numpy(), index=df.index)
    if origin.isna().any():
        raise ValueError("La serie INPC no cubre todos los periodos de origen.")
    result = df.copy()
    result["factor_inpc"] = monthly.loc[target] / origin
    for c in cols:
        number = pd.to_numeric(df[c], errors="coerce")
        if (number.isna() & df[c].notna()).any():
            raise ValueError(f"La columna {c} contiene importes no numéricos.")
        result[f"{c}_ajustada"] = number * result["factor_inpc"]
    return result
