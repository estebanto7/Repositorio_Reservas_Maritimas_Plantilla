"""Auditoría inicial. No se eliminan datos automáticamente."""
from __future__ import annotations
import pandas as pd


def resumen_calidad(df: pd.DataFrame) -> pd.DataFrame:
    """Resume tipos, nulos, ceros, negativos y distintos por columna."""
    out = pd.DataFrame(index=df.columns)
    out.index.name = "variable"
    out["tipo"] = df.dtypes.astype(str)
    out["nulos"] = df.isna().sum()
    out["unicos"] = df.nunique(dropna=True)
    out["ceros"] = [int((df[c] == 0).sum()) if pd.api.types.is_numeric_dtype(df[c]) else pd.NA for c in df]
    out["negativos"] = [int((df[c] < 0).sum()) if pd.api.types.is_numeric_dtype(df[c]) else pd.NA for c in df]
    return out


def normalizar_espacios(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Devuelve copia con espacios externos/internos normalizados.

    No fusiona categorías que difieren por tildes, mayúsculas o semántica.
    """
    out = df.copy()
    for col in columnas:
        if col not in out:
            raise KeyError(col)
        out[col] = out[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    return out
