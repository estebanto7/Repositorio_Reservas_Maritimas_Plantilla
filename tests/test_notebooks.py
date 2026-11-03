import json
from pathlib import Path

NOTEBOOKS = [
    "00_revision_datos.ipynb",
    "01_actualizacion_inpc.ipynb",
    "02_analisis_mercado.ipynb",
    "03_siniestralidad_conglomerados.ipynb",
    "04_calculo_reservas.ipynb",
]


def test_notebooks_requeridos_son_json_validos():
    root = Path(__file__).resolve().parents[1]
    for nombre in NOTEBOOKS:
        ruta = root / "notebooks" / nombre
        data = json.loads(ruta.read_text(encoding="utf-8"))
        assert data["nbformat"] >= 4
        assert data["cells"]


def test_notebooks_no_dependen_de_variables_de_otro_notebook():
    root = Path(__file__).resolve().parents[1]
    for nombre in NOTEBOOKS:
        texto = (root / "notebooks" / nombre).read_text(encoding="utf-8")
        assert "ADA RESERVAS.ipynb" not in texto
        assert "cargar_excel" not in texto
        assert '"/src/"' not in texto
