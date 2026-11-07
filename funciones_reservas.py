"""Funciones sencillas para el análisis de reservas marítimas."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans, AgglomerativeClustering
from kmedoids import KMedoids

from sklearn.metrics import silhouette_score, calinski_harabasz_score


def resumen_calidad(df):

    resumen = pd.DataFrame({
        "tipo": df.dtypes,
        "nulos": df.isna().sum(),
        "unicos": df.nunique()
    })

    resumen["ceros"] = [
        (df[col] == 0).sum()
        if pd.api.types.is_numeric_dtype(df[col])
        else "—"
        for col in df.columns
    ]

    resumen["negativos"] = [
        (df[col] < 0).sum()
        if pd.api.types.is_numeric_dtype(df[col])
        else "—"
        for col in df.columns
    ]

    return resumen


def normalizar_espacios(df: pd.DataFrame, columnas: Iterable[str]) -> pd.DataFrame:
    """Copia el DataFrame y normaliza espacios sin borrar observaciones."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un DataFrame de pandas.")
    columnas = list(columnas)
    faltantes = [col for col in columnas if col not in df]
    if faltantes:
        raise KeyError(f"Columnas no encontradas: {faltantes}")
    out = df.copy()
    for col in columnas:
        out[col] = out[col].astype("string").str.strip().str.replace(
            r"\s+", " ", regex=True
        )
    return out


def normalizar_categorias(
    df: pd.DataFrame,
    columnas: Iterable[str],
    *,
    minusculas: bool = True,
    quitar_acentos: bool = False,
) -> pd.DataFrame:
    """Normaliza categorías textuales conservando filas y valores faltantes."""
    out = normalizar_espacios(df, columnas)
    for col in columnas:
        valores = out[col]
        if minusculas:
            valores = valores.str.lower()
        if quitar_acentos:
            valores = valores.map(
                lambda value: (
                    unicodedata.normalize("NFKD", value)
                    .encode("ascii", "ignore")
                    .decode("ascii")
                    if pd.notna(value)
                    else value
                )
            )
        out[col] = valores
    return out


# Actualización por INPC
def ajustar_inpc(
    df: pd.DataFrame,
    columnas: str | list[str],
    fecha_col: str,
    fecha_objetivo: str | int,
    inpc: pd.Series,
    frecuencia: str = "anual",
    criterio_anual: str = "diciembre",
) -> pd.DataFrame:
    """Actualiza importes sin sobrescribir las columnas originales."""
    if not isinstance(df, pd.DataFrame) or not isinstance(inpc, pd.Series):
        raise TypeError("df debe ser DataFrame e inpc debe ser Series de pandas.")
    cols = [columnas] if isinstance(columnas, str) else list(columnas)
    if not cols or len(set(cols)) != len(cols):
        raise ValueError("Indica columnas únicas y no vacías.")
    missing = [col for col in [fecha_col, *cols] if col not in df]
    if missing:
        raise KeyError(f"Columnas no encontradas: {missing}")
    if frecuencia not in {"anual", "mensual", "diaria"}:
        raise ValueError("frecuencia debe ser anual, mensual o diaria.")
    if criterio_anual not in {"diciembre", "promedio"}:
        raise ValueError("criterio_anual debe ser diciembre o promedio.")

    salidas = [f"{col}_ajustada" for col in cols] + ["factor_inpc"]
    if any(col in df for col in salidas):
        raise ValueError("Algunas columnas de salida ya existen en el DataFrame.")

    objetivo = str(fecha_objetivo).strip()
    if re.fullmatch(r"\d{4}", objetivo):
        objetivo += "-12"
    objetivo = pd.to_datetime(objetivo, errors="coerce")
    if pd.isna(objetivo):
        raise ValueError("fecha_objetivo inválida.")
    objetivo = objetivo.to_period("M")

    if isinstance(inpc.index, pd.PeriodIndex):
        indice = inpc.index.asfreq("M")
    else:
        if pd.api.types.is_numeric_dtype(inpc.index.dtype):
            raise ValueError("Los índices del INPC deben tener fechas, no números.")
        fechas = pd.to_datetime(inpc.index, errors="coerce")
        if pd.isna(fechas).any():
            raise ValueError("Índice temporal del INPC inválido.")
        indice = fechas.to_period("M")
    if indice.has_duplicates:
        raise ValueError("Hay meses repetidos en la serie INPC.")
    valores = pd.to_numeric(inpc.to_numpy(), errors="coerce")
    if pd.isna(valores).any() or (valores <= 0).any():
        raise ValueError("Los valores INPC deben ser positivos y válidos.")
    mensual = pd.Series(valores, index=indice).sort_index()
    if objetivo not in mensual:
        raise ValueError(f"No existe INPC para el destino {objetivo}.")

    if frecuencia == "anual":
        raw = df[fecha_col].astype("string").str.strip()
        years = pd.to_numeric(raw, errors="coerce")
        valid = raw.str.fullmatch(r"\d{4}(?:\.0+)?").fillna(False)
        if not valid.all() or years.isna().any() or not years.between(1000, 9999).all():
            raise ValueError(
                "Para frecuencia anual, fecha_col debe contener años de cuatro cifras."
            )
        years = years.astype(int)
        if criterio_anual == "diciembre":
            periodos = pd.PeriodIndex([f"{year}-12" for year in years], freq="M")
            origen = pd.Series(mensual.reindex(periodos).to_numpy(), index=df.index)
        else:
            cantidad = mensual.groupby(mensual.index.year).size()
            faltan = sorted({year for year in years if cantidad.get(year, 0) != 12})
            if faltan:
                raise ValueError(
                    f"Faltan INPC mensuales para calcular promedio anual: {faltan}"
                )
            anual = mensual.groupby(mensual.index.year).mean()
            origen = pd.Series(years.map(anual).to_numpy(), index=df.index)
    else:
        raw = df[fecha_col].astype("string").str.strip()
        fechas = pd.to_datetime(raw, errors="coerce", dayfirst=True, format="mixed")
        if fechas.isna().any():
            raise ValueError("Hay fechas de origen inválidas.")
        periodos = pd.PeriodIndex(fechas.dt.to_period("M"), freq="M")
        origen = pd.Series(mensual.reindex(periodos).to_numpy(), index=df.index)

    if origen.isna().any():
        raise ValueError("La serie INPC no cubre todos los periodos de origen.")
    result = df.copy()
    result["factor_inpc"] = mensual.loc[objetivo] / origen
    for col in cols:
        numero = pd.to_numeric(df[col], errors="coerce")
        if (numero.isna() & df[col].notna()).any():
            raise ValueError(f"La columna {col} contiene importes no numéricos.")
        result[f"{col}_ajustada"] = numero * result["factor_inpc"]
    return result


# Snapshots y reproducibilidad
def _hash_archivo(ruta: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(ruta).open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()


def guardar_snapshot(
    df: pd.DataFrame,
    ruta: str | Path,
    *,
    periodo_valuacion: str,
    fuente_inpc: str | None = None,
    criterio_actualizacion: str | None = None,
    version: str = "1",
    archivos_origen: Iterable[str | Path] = (),
) -> Path:
    """Guarda un snapshot Parquet y un JSON mínimo de reproducibilidad."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un DataFrame de pandas.")
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)
    metadata = {
        "periodo_valuacion": periodo_valuacion,
        "fuente_inpc": fuente_inpc,
        "criterio_actualizacion": criterio_actualizacion,
        "version_procesamiento": version,
        "archivos_origen": {
            str(Path(origen)): _hash_archivo(origen)
            for origen in archivos_origen
            if Path(origen).exists()
        },
    }
    ruta.with_suffix(".json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return ruta


def snapshot_es_valido(
    ruta: str | Path,
    *,
    periodo_valuacion: str,
    version: str = "1",
    archivos_origen: Iterable[str | Path] = (),
) -> bool:
    """Comprueba existencia, metadatos y hashes de un snapshot."""
    ruta = Path(ruta)
    metadata_ruta = ruta.with_suffix(".json")
    if not ruta.exists() or not metadata_ruta.exists():
        return False
    try:
        metadata = json.loads(metadata_ruta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if metadata.get("periodo_valuacion") != periodo_valuacion:
        return False
    if metadata.get("version_procesamiento") != version:
        return False
    for origen in archivos_origen:
        origen = Path(origen)
        hashes = metadata.get("archivos_origen", {})
        if not origen.exists() or hashes.get(str(origen)) != _hash_archivo(origen):
            return False
    return True


def leer_snapshot(ruta: str | Path) -> pd.DataFrame:
    """Lee un snapshot existente o informa exactamente qué falta."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el snapshot: {ruta}")
    return pd.read_parquet(ruta)


# Resúmenes y exportación
def resumen_emision_anual(df: pd.DataFrame, anio: str = "año") -> pd.DataFrame:
    """Suma importes y calcula crecimiento, retención y comisiones."""
    columnas = [
        "prima_emitida_ajustada",
        "prima_retenida_ajustada",
        "comision_directa_ajustada",
    ]
    faltantes = [col for col in [anio, *columnas] if col not in df]
    if faltantes:
        raise KeyError(f"Columnas no encontradas: {faltantes}")
    agregado = df.groupby(anio, dropna=False)[columnas].sum().sort_index()
    for col, etiqueta in [
        (columnas[0], "crecimiento_emitida_pct"),
        (columnas[1], "crecimiento_retenida_pct"),
    ]:
        anterior = agregado[col].shift()
        agregado[etiqueta] = np.where(
            anterior > 0, (agregado[col] / anterior - 1) * 100, np.nan
        )
    base = agregado[columnas[0]].where(agregado[columnas[0]] > 0)
    agregado["retencion_pct"] = agregado[columnas[1]] / base * 100
    agregado["comisiones_pct"] = agregado[columnas[2]] / base * 100
    return agregado.reset_index()


def participacion_por_categoria(
    df: pd.DataFrame, categoria: str = "tipo_embarcacion"
) -> pd.DataFrame:
    """Calcula participaciones netas y conserva categorías con importes negativos."""
    requeridas = ["año", categoria, "prima_emitida_ajustada"]
    faltantes = [col for col in requeridas if col not in df]
    if faltantes:
        raise KeyError(f"Columnas no encontradas: {faltantes}")
    agregado = (
        df.groupby(["año", categoria], dropna=False)["prima_emitida_ajustada"]
        .sum()
        .unstack(fill_value=0)
    )
    total = agregado.sum(axis=1)
    if (total <= 0).any():
        raise ValueError("Hay años cuya emisión neta total no es positiva.")
    return agregado.div(total, axis=0).mul(100)


def evaluar_modelo(X, metodo, k_max):
    """
    Evalúa un método de clustering para k = 2 hasta k_max.

    Retorna un DataFrame con:
    - Silhouette
    - Calinski-Harabasz
    - WCSS
    - Tamaños de los grupos
    - Tamaño del grupo más pequeño

    Parameters
    ----------
    metodo : str
        Método de clustering a evaluar. Puede ser "Ward", "Liga completa", "K-means" o "K-medoids".
    """

    X = np.asarray(X)
    resultados = []

    for k in range(2, k_max + 1):

        # Seleccionar modelo
        modelos = {
            "Ward": AgglomerativeClustering(
                n_clusters=k, linkage="ward"
            ),

            "Liga completa": AgglomerativeClustering(
                n_clusters=k, linkage="complete"
            ),

            "K-means": KMeans(
                n_clusters=k, random_state=42, n_init=20
            ),

            "K-medoids": KMedoids(
                n_clusters=k, metric="euclidean",
                method="pam", random_state=42
            )
        }

        if metodo not in modelos:
            raise ValueError(f"Método no válido: {metodo}")

        # Ajustar modelo para este k
        modelo = modelos[metodo]
        etiquetas = modelo.fit_predict(X)

        # Métricas
        silhouette = silhouette_score(X, etiquetas)
        calinski = calinski_harabasz_score(X, etiquetas)

        # WCSS: suma de cuadrados respecto a los centroides
        wcss = 0

        for grupo in np.unique(etiquetas):
            puntos = X[etiquetas == grupo]
            centroide = puntos.mean(axis=0)

            wcss += ((puntos - centroide) ** 2).sum()

        # Tamaño de los grupos
        tamanos = np.bincount(etiquetas)
        tamanos = np.sort(tamanos)[::-1]

        # Guardar resultados
        resultados.append({
            "Número de clusters": k,
            "Silhouette": silhouette,
            "Calinski-Harabasz": calinski,
            "WCSS": wcss,
            "Tamaño de grupos": tamanos.tolist(),
            "Grupo mínimo": tamanos.min()
        })

    return pd.DataFrame(resultados).round(3)