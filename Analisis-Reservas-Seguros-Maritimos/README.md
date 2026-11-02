# Análisis del mercado y reservas de seguros marítimos

**Estudio actuarial de primas, siniestros, siniestralidad, segmentación y reservas — 2015–2025**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white) ![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-64748b)

> **Estado:** proyecto académico en desarrollo. El repositorio ofrece una estructura reproducible; los resultados finales se añadirán cuando estén verificados. No contiene bases originales ni resultados inventados.

## 1. Objetivo

Estudiar el comportamiento del mercado de seguros de embarcaciones y comparar métodos actuariales para estimar reservas al **31 de diciembre de 2025**. El análisis distingue entre cifras de emisión, siniestros por año de origen y pólizas con vigencia exacta.

### Preguntas del estudio

- ¿Cómo ha evolucionado la prima emitida en términos reales?
- ¿Qué relación tienen las comisiones y primas retenidas con las primas emitidas?
- ¿Cómo cambia la composición de la emisión por tipo o uso de embarcación?
- ¿Qué años y causas concentran mayores pagos por siniestros?
- ¿Qué perfiles de siniestralidad anual se parecen entre sí?
- ¿Cómo difieren las reservas estimadas mediante distintos métodos?

## 2. Ruta del proyecto

| Apartado | Pregunta principal | Estado |
|---|---|---|
| 1. Actualización monetaria | ¿Cómo comparar importes de diferentes años? | En desarrollo |
| 2. Emisión | ¿Cómo cambian primas, comisiones, retención y composición? | En desarrollo |
| 3. Siniestros | ¿Cuándo y por qué se pagan más siniestros? | En desarrollo |
| 4. Siniestralidad y conglomerados | ¿Qué grupos muestran patrones similares? | Pendiente |
| 5. Reserva de Riesgos en Curso | ¿Cuál es la reserva al cierre de 2025? | Pendiente |
| 6. Reserva de SONR | ¿Qué estiman Chain Ladder, razón y estatutario? | Pendiente |
| 7. Conclusiones | ¿Qué implican los resultados y cuáles son sus límites? | Pendiente |

*SONR: siniestros ocurridos no reportados. La diferencia entre pagos observados y siniestralidad última se documentará antes del cálculo.*

## 3. Datos

Se utilizan **dos fuentes con fines distintos**:

1. **Base histórica de reservas:** hojas `EMISION` y `SINIESTRALIDAD`, para estudiar la evolución anual y los desarrollos de pagos.
2. **Base de pólizas de 2025:** registros con `inicio_vigencia` y `fin_vigencia`, necesarios para el análisis de riesgos en curso; debe verificarse la integridad del universo de pólizas vigentes al cierre.

Los archivos originales **no están incluidos**. Consulta [`data/README.md`](data/README.md), el [diccionario de datos](docs/diccionario_datos.md) y las [decisiones metodológicas](docs/decisiones_metodologicas.md) antes de ejecutar los notebooks.

## 4. Estructura

```text
.
├── README.md                     # Portada y visión general
├── requirements.txt              # Dependencias
├── .gitignore                    # Archivos que no se publican
├── .github/workflows/tests.yml   # Verificación automática
├── data/
│   ├── README.md                 # Origen, rutas y restricciones
│   ├── raw/                      # Datos originales (ignorados)
│   └── processed/                # Datos de trabajo (ignorados)
├── notebooks/
│   ├── 00_revision_datos.ipynb
│   ├── 01_actualizacion_inpc.ipynb
│   ├── 02_analisis_mercado.ipynb
│   ├── 03_siniestralidad_conglomerados.ipynb
│   └── 04_calculo_reservas.ipynb
├── src/reservas_maritimas/
│   ├── inpc.py                    # Ajuste monetario reusable
│   ├── calidad.py                 # Auditoría de datos
│   └── mercado.py                 # Agregaciones e indicadores
├── tests/                        # Pruebas con datos sintéticos
├── docs/                         # Metodología y decisiones
└── reports/figures/              # Gráficas exportadas
```

## 5. Cómo ejecutarlo (VS Code / Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Abre la carpeta en VS Code, selecciona el entorno `.venv` como kernel de Jupyter y comienza con `notebooks/00_revision_datos.ipynb`. Copia tu notebook existente a `notebooks/` o traslada las celdas por apartados; **no hace falta reescribir tu trabajo desde cero**.

> Si instalaste Python con otro nombre, sustituye `py` por `python`.

## 6. Implementaciones reutilizables

El módulo `src/reservas_maritimas/inpc.py` permite ajustar columnas monetarias con una serie mensual de INPC facilitada por el usuario, sin descargar índices automáticamente ni ocultar supuestos temporales. Incluye cálculo de factores y preservación de valores originales.

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd().resolve() / "src"))
from reservas_maritimas.inpc import ajustar_inpc

# Se requiere tener `datos` y `serie_inpc` ya cargados.
resultado = ajustar_inpc(
    df=datos,
    columnas=["prima_emitida"],
    fecha_col="año",
    fecha_objetivo="2025-12",
    inpc=serie_inpc,
    frecuencia="anual",
    criterio_anual="diciembre"
)
```

**Importante:** este ejemplo supone que se ejecuta desde la raíz del proyecto. En notebooks se recomienda usar la celda de configuración incluida para localizar `src`.

## 7. Calidad y límites del análisis

- Los **montos negativos** no se borran automáticamente: pueden corresponder a devoluciones, cancelaciones o correcciones que deben validarse.
- Los ceros de desarrollo de siniestros no necesariamente significan que el siniestro no generará pagos futuros.
- El INPC es mensual; un año de emisión no equivale necesariamente a una fecha de emisión o de valuación al cierre.
- El año de **origen** y el año de **pago** son dimensiones distintas: para desarrollos anuales, año calendario ≈ origen + desarrollo, sujeto a confirmación.
- El estudio de conglomerados se plantea sobre **factores anuales de siniestralidad**, no sobre montos monetarios brutos ni como paso obligatorio de Chain Ladder.
- Una gráfica de participación relativa no basta para concluir que aumentaron los montos absolutos de un segmento.
- Ningún resultado de reserva debe presentarse como cálculo definitivo sin contrastar datos, definiciones y supuestos de las instrucciones.

Ver [metodología](docs/metodologia.md) y [registro de decisiones](docs/decisiones_metodologicas.md).

## 8. Resultados y visualizaciones

Las visualizaciones verificadas se incorporarán en `reports/figures/` y se enlazarán aquí con su interpretación, su unidad de medida, su fecha de corte y su fuente. **No se muestran resultados hasta revisarlos.**

## 9. Fuentes y referencias

- INEGI — Índice Nacional de Precios al Consumidor (INPC).
- Banco de México — Sistema de Información Económica (SIE), para consulta de series.
- Instrucciones de la actividad y anexos regulatorios proporcionados por la docente: Anexo 5.3.1 y Anexo 8.20.2 (verificar versión aplicable antes de concluir).

## 10. Autoría, uso y licencias

Proyecto académico. Completa los créditos del autor o equipo en `docs/creditos.md`. **Aún no se incluye una licencia de código**: elige una con conocimiento de sus implicaciones antes de publicar. Verifica que tengas permiso para difundir bases, capturas y material de terceros.
