# Metodología

## Alcance

El estudio cubre el mercado de seguros de embarcaciones en México entre 2015 y 2025. La fecha de valuación de las reservas es el 31/12/2025. La base histórica contiene emisión y siniestralidad; la base de 2025 contiene fechas exactas de vigencia para el análisis de Riesgos en Curso.

## Revisión y limpieza

Se inspeccionan dimensiones, tipos, nulos, duplicados, ceros, negativos y categorías. La normalización de texto quita espacios repetidos y unifica mayúsculas sin eliminar filas. Los importes negativos se conservan porque pueden representar cancelaciones, devoluciones o ajustes contables. Los faltantes se tratan según la variable necesaria, no mediante `dropna()` general.

## Actualización por INPC

La función `ajustar_inpc()` usa una serie mensual positiva y calcula:

`importe ajustado = importe original × INPC destino / INPC origen`.

Para registros anuales se utiliza diciembre del año de origen y diciembre de 2025 como destino. La serie faltante no se imputa. En siniestros se distingue el año de origen del año de pago; se usa `año de origen + desarrollo` únicamente como regla de trabajo pendiente de confirmación. Los desarrollos 0 a 3 no se consideran acumulados sin evidencia.

## Emisión y siniestros

Se agregan primas emitidas, retenidas y comisiones por año. El crecimiento se omite si la base previa no es positiva. Retención y comisiones se calculan respecto de la prima emitida positiva. Las participaciones pueden ser negativas cuando existen importes netos negativos; por ello una gráfica apilada al 100% debe interpretarse con cautela.

Los índices comparativos toman 2015 como base 100. Las gráficas de siniestros muestran montos observados por año de origen y causa, sin afirmar que los últimos años tengan la misma maduración.

## Siniestralidad y conglomerados

El factor deberá relacionar siniestros con prima emitida por año y segmento. Antes de calcularlo se debe confirmar si los importes de desarrollo son incrementales o acumulados, cómo tratar prima cero y si se usa pago observado o monto último. Los conglomerados se construirán con factores anuales, no con montos brutos, y se justificarán estandarización, distancia, método y estabilidad.

## Reserva de Riesgos en Curso

La base de emisión de 2025 se revisará con `inicio_vigencia` y `fin_vigencia`. Antes de aplicar método exacto, veinticuatroavos o estatutario se debe confirmar el universo de pólizas, prima aplicable, gastos, siniestralidad y reglas del anexo correspondiente.

## SONR

Se debe validar el triángulo, distinguir pagos de incurridos y confirmar su naturaleza incremental o acumulada. Solo después se compararán Chain Ladder, método de la razón y método estatutario al 31/12/2025.

## Reproducibilidad y límites

Los snapshots guardan periodo de valuación, criterio de actualización, fuente INPC, versión de procesamiento y hashes de archivos de origen. Se invalidan cuando cambia una fuente. Los resultados pendientes se mantienen como pendientes y las hipótesis sobre pandemia, huracanes o conflictos geopolíticos no se presentan como causalidades demostradas.
