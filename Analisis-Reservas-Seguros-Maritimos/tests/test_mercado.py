import pandas as pd
import pytest
from reservas_maritimas.calidad import normalizar_espacios, resumen_calidad
from reservas_maritimas.mercado import resumen_emision_anual, participacion_por_categoria


def test_limpieza_espacios_sin_mutar_original():
    df = pd.DataFrame({"tipo_embarcacion": [" Abastecedor  ", "Abastecedor"]})
    out = normalizar_espacios(df, ["tipo_embarcacion"])
    assert out["tipo_embarcacion"].nunique() == 1
    assert df.iloc[0, 0] != out.iloc[0, 0]


def test_sumar_con_negativos():
    df = pd.DataFrame({"año": [2024, 2024], "tipo_embarcacion": ["A", "B"],
        "prima_emitida_ajustada": [100, -10], "prima_retenida_ajustada": [50, 0], "comision_directa_ajustada": [5, -1]})
    out = resumen_emision_anual(df)
    assert out["prima_emitida_ajustada"].iloc[0] == 90
    part = participacion_por_categoria(df)
    assert part.loc[2024, "B"] == pytest.approx(-100/9)
    assert part.loc[2024].sum() == pytest.approx(100)
    assert resumen_calidad(df).loc["prima_emitida_ajustada", "negativos"] == 1
