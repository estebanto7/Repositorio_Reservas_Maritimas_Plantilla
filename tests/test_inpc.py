import pandas as pd
import pytest

from funciones_reservas import ajustar_inpc


def test_inpc_anual_diciembre_y_signo():
    serie = pd.Series([100.0, 110.0], index=pd.to_datetime(["2024-12-01", "2025-12-01"]))
    df = pd.DataFrame({"año": [2024, 2025], "prima": [1000.0, -200.0]})
    r = ajustar_inpc(df, "prima", "año", 2025, serie)
    assert list(r["prima_ajustada"]) == pytest.approx([1100.0, -200.0])
    assert "prima_ajustada" not in df


def test_inpc_promedio_exige_12_meses():
    serie = pd.Series([100.0, 110.0], index=pd.to_datetime(["2024-12-01", "2025-12-01"]))
    with pytest.raises(ValueError, match="Faltan INPC"):
        ajustar_inpc(pd.DataFrame({"año": [2024], "prima": [100]}), "prima", "año", 2025, serie, criterio_anual="promedio")


def test_inpc_fecha_mensual():
    serie = pd.Series([100., 120.], index=pd.to_datetime(["2025-01-01", "2025-12-01"]))
    df = pd.DataFrame({"fecha": ["2025-01", "2025-12"], "importe": [100, 100]})
    r = ajustar_inpc(df, "importe", "fecha", "2025-12", serie, frecuencia="mensual")
    assert r["importe_ajustada"].tolist() == pytest.approx([120, 100])


def test_inpc_conserva_filas_y_montos_faltantes():
    serie = pd.Series([100.0, 110.0], index=pd.to_datetime(["2024-12-01", "2025-12-01"]))
    df = pd.DataFrame({"año": [2024, 2024], "prima": [100.0, None]})
    r = ajustar_inpc(df, "prima", "año", 2025, serie)
    assert len(r) == len(df)
    assert pd.isna(r.loc[1, "prima_ajustada"])
