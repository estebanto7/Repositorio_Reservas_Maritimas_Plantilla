"""Cálculos exploratorios: los denominadores se validan explícitamente."""
from __future__ import annotations
import numpy as np
import pandas as pd


def resumen_emision_anual(df: pd.DataFrame, anio="año") -> pd.DataFrame:
    """Suma primas/comisiones ajustadas y calcula indicadores anuales.

    Los cocientes se dejan NaN si la emisión total anual es <= 0.
    Las tasas de crecimiento se omiten cuando la base previa es <= 0.
    """
    cols = ["prima_emitida_ajustada", "prima_retenida_ajustada", "comision_directa_ajustada"]
    ag = df.groupby(anio, dropna=False)[cols].sum().sort_index()
    for c, tag in [(cols[0], "crecimiento_emitida_pct"), (cols[1], "crecimiento_retenida_pct")]:
        prev = ag[c].shift()
        ag[tag] = np.where(prev > 0, (ag[c] / prev - 1) * 100, np.nan)
    base = ag[cols[0]].where(ag[cols[0]] > 0)
    ag["retencion_pct"] = ag[cols[1]] / base * 100
    ag["comisiones_pct"] = ag[cols[2]] / base * 100
    return ag.reset_index()


def participacion_por_categoria(df: pd.DataFrame, categoria="tipo_embarcacion") -> pd.DataFrame:
    """Calcula participaciones netas con todas las categorías.

    Nota: pueden existir participaciones negativas, por tanto un área 100% apilada
    no siempre es una representación apropiada.
    """
    ag = df.groupby(["año", categoria], dropna=False)["prima_emitida_ajustada"].sum().unstack(fill_value=0)
    total = ag.sum(axis=1)
    if (total <= 0).any():
        raise ValueError("Hay años cuya emisión neta total no es positiva.")
    return ag.div(total, axis=0).mul(100)
