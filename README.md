# Mercado y reservas de seguros marítimos

Proyecto académico de Actuaría sobre el mercado mexicano de seguros de embarcaciones durante **2015-2025**, con fecha de valuación **31 de diciembre de 2025**.

## Objetivo

Revisar las bases, actualizar importes mediante INPC, analizar emisión y siniestros, y dejar preparados los cálculos de siniestralidad, Reserva de Riesgos en Curso y SONR. No se presentan resultados pendientes ni datos inventados.

## Datos

- `data/raw/2026 BASE RESERVAS.xlsx`: hojas `EMISION` y `SINIESTRALIDAD`.
- `data/raw/EMISION 2025.xlsx`: pólizas 2025 con inicio y fin de vigencia.
- `data/processed/`: snapshots Parquet generados localmente.
## Notebooks

1. [00_revision_datos.ipynb](notebooks/00_revision_datos.ipynb): inspección, calidad y categorías.
2. [01_actualizacion_inpc.ipynb](notebooks/01_actualizacion_inpc.ipynb): INPC y snapshots ajustados.
3. [02_analisis_mercado.ipynb](notebooks/02_analisis_mercado.ipynb): primas, comisiones, composición y siniestros.
4. [03_siniestralidad_conglomerados.ipynb](notebooks/03_siniestralidad_conglomerados.ipynb): estructura pendiente para factores y grupos.
5. [04_calculo_reservas.ipynb](notebooks/04_calculo_reservas.ipynb): estructura pendiente para RRC y SONR.

## Estructura

```text
.
├── data/raw/                 # Excel locales
├── data/processed/           # snapshots locales
├── notebooks/                # análisis reproducibles
├── src/funciones_reservas.py # funciones reutilizables
├── tests/                    # pruebas con datos sintéticos
├── reports/figures/          # gráficas exportadas localmente
├── reports/tables/           # tablas exportadas localmente
├── METODOLOGIA.md
└── AGENTS.md
```

## Instalación y ejecución

En Windows, desde esta carpeta:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Después abre los notebooks en VS Code y ejecútalos de forma independiente. El notebook 01 requiere una serie mensual de INPC y, si se descarga desde Banxico, la configuración correspondiente de [`banxicolab`](https://github.com/AnaJZP/banxicolab) se tiene que configurar el token y generar uno personal en (https://www.banxico.org.mx/SieAPIRest/service/v1/token). Si falta, muestra el requisito y no inventa snapshots. 
