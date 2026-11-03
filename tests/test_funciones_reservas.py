import json

import pandas as pd
import pytest

from funciones_reservas import (
    guardar_snapshot,
    leer_snapshot,
    snapshot_es_valido,
)


def test_snapshot_se_guarda_se_lee_y_conserva_metadatos(tmp_path):
    origen = tmp_path / "origen.xlsx"
    origen.write_bytes(b"base sintetica")
    ruta = tmp_path / "procesado.parquet"
    esperado = pd.DataFrame({"año": [2025], "importe": [-10.0]})

    guardar_snapshot(
        esperado,
        ruta,
        periodo_valuacion="2025-12",
        fuente_inpc="serie sintetica",
        criterio_actualizacion="diciembre",
        archivos_origen=[origen],
    )

    pd.testing.assert_frame_equal(leer_snapshot(ruta), esperado)
    metadata = json.loads(ruta.with_suffix(".json").read_text(encoding="utf-8"))
    assert metadata["periodo_valuacion"] == "2025-12"
    assert snapshot_es_valido(
        ruta,
        periodo_valuacion="2025-12",
        archivos_origen=[origen],
    )


def test_snapshot_invalido_si_cambia_la_fuente(tmp_path):
    origen = tmp_path / "origen.xlsx"
    origen.write_bytes(b"version 1")
    ruta = tmp_path / "procesado.parquet"
    guardar_snapshot(
        pd.DataFrame({"importe": [1]}),
        ruta,
        periodo_valuacion="2025-12",
        archivos_origen=[origen],
    )
    origen.write_bytes(b"version 2")
    assert not snapshot_es_valido(
        ruta,
        periodo_valuacion="2025-12",
        archivos_origen=[origen],
    )


def test_lectura_de_snapshot_inexistente_es_explicita(tmp_path):
    with pytest.raises(FileNotFoundError, match="No existe el snapshot"):
        leer_snapshot(tmp_path / "faltante.parquet")
