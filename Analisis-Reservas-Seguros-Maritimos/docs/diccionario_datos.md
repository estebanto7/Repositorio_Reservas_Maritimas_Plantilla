# Diccionario de datos (preliminar)

> Verifica cada definición con la fuente antes de publicar resultados. La base no informa por sí sola el significado contable de los signos negativos ni si los montos de desarrollo son incrementales o acumulados.

| Hoja | Campo | Descripción operativa | Tipo previsto |
|---|---|---|---|
| EMISION | `año` | Año consignado en el registro de emisión | entero |
| EMISION | `tipo_embarcacion` | Clase de embarcación; requiere normalización textual | texto |
| EMISION | `uso` | Uso declarado; requiere normalización textual | texto |
| EMISION | `anio_construccion` | Año de construcción de la embarcación | entero |
| EMISION | `prima_emitida` | Monto monetario registrado de prima emitida | numérico |
| EMISION | `prima_retenida` | Monto monetario registrado de prima retenida | numérico |
| EMISION | `comision_directa` | Monto monetario de comisión directa | numérico |
| SINIESTRALIDAD | `año` | Presunto año de origen del siniestro, pendiente de confirmar | entero |
| SINIESTRALIDAD | `causa_siniestro` | Causa reportada, si está disponible con ese nombre | texto |
| SINIESTRALIDAD | `tipo_embarcacion`, `uso` | Categorías de embarcación | texto |
| SINIESTRALIDAD | `0_monto pagado` … `3_monto pagado` | Montos por desarrollo 0–3; verificar definición | numérico |
| EMISION 2025 | `inicio_vigencia`, `fin_vigencia` | Fechas exactas del periodo de cobertura | fecha |

Cambia los nombres de columnas en el código si tus encabezados reales difieren de los aquí mostrados.
