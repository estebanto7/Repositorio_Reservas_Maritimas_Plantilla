# ¿Cuál es el objetivo general de la actividad?

Consiste en analizar el comportamiento de un mercado de seguros de embarcaciones y calcular las reservas que necesita una aseguradora para cumplir con sus obligaciones*

Se puede dividir en 3 grandes partes:

## Análisis del mercado (1, 2, 3)
Estudiar las primas cobradas, los siniestros y su comportamiento a través de los años

## Siniestralidad y Conglomerados (4)
Medir que tan grandes son los siniestros respecto a las primas y agrupar tipos de embarcaciones con comportamientos similares

## Calculo de Reservas (5, 6) 
Estimar cuánto dinero se necesita reservar para riesgos aún vigentes y siniestros ocurridos todavía no reportados


Datos de primas y siniestros (por año y tipo de embarcación)
 ---> Calcular factores de siniestralidad anual (Siniestros totales / primas emitidas)
 ---> Análisis de conglomerados (Agrupar tipos de embarcación con factores anuales semejantes, por ejemplo mediante Ward con distancia euclidiana)
---> Chain Ladder, por separado (Construir triángulos de desarrollo y proyectar siniestros para estimar la reserva solicitada)


# ¿Qué se pide en cada apartado?

## 1. Actualización de cifras
**Se busca:** que la inflación no distorsione las comparaciones entre años

- LLevar los montos monetarios de distintos años a una base comparable, indicando el factor de actualización y su fiente, por ejemplo, mediante el INPC **(Crear una función para convertir una base de datos a cifras comparables)**


## 2. Análisis de la prima emitida
**Se busca**: entender cómo se comporta el volumen de primas del mercado y como esta distribuido

- a) Ver como aumenta o disminuye la prima emitida total por año **(Line chart)**
- b) Comparar las comisiones directas con las primas emitidas  
- c) Comparar las primas retenidas con las emitidas
- d) Analizar la distribución de primas por tipo de embarcación, identificando cuáles aprotan más o menos y cómo cambian con el tiempo

## 3. Análisis del monto de siniestros
**Se busca**: entender cúando ocurren mayores périddas y cuáles son sus principales causas

- a) Calcular cuánto suman los siniestros de cada año y estudiar su tendencia
- b) Identificar las principales causas de siniestros y cuánto representan del total anual 

## 4. Factores de siniestralidad y conglomerados
**Se busca:** reconocer qué segmentos presentan siniestralidad alta, baja o comportamientos similares 

$$ Siniestralidad = \frac{Siniestros totales}{Prima emitida}$$

- a) Calcular la siniestralidad anual por tipo de embarcaci[on y para todo el mercado
- b) Comparar estos factores entre años, identificando máximos, mínimos, valores atípicos y cambios
- Agrupar los tipos de embarcaciones según sus factores anuales de siniestraldiad **(Análisis 
de Conglomerados)**

## 5. Reserva de Riesgos en Curso (RRC)
**Se busca:** estimar la reserva necesaria para cubrir obligaciones futuras por pólizas que siguen vigentes, comparando los resultados de los tres métodos

- Calcular al 31 de diciembre de 2025 cuánto dinero corresponde a riesgos que todavía estan cubiertos por pólizas vigentes.
- Se comparan tres métodos: exacto, venticuatroavos y estatutario

## 6. Reserva de siniestros ocurridos no reportados (SONR)
**Se busca**: estimar estas obligaciones pendientes con diferentes metodologías y explicar las diferencias 

- Calcular al 31 de diciembre de 2025 la reserva correspondiente a siniestros que ya ocurrieron, pero todavía no se reportaron.
- Se compara Chain Ladder, método de la razón y método estatutario

## 7. Conclusiones 
**Se busca:** interpretar qué aprendiste del comportamiento del mercado, sus riesgos, su segmentación y sus reservas

Explicar los prinicpales resultados de cada uno de los seis apartados anteriores. 

# Metodología de Clusters

## Antes de comenzar: Decisiones metodológicas
- Definir las características que utilizaremos.
- Establecer cómo comparar las variables entre ventanas.
- Definir los criterios para evaluar la estabilidad.

## Etapa 1: Construcción de nuevas variables
- Siniestralidad acumulada.
- Variabilidad temporal.
- Recurrencia de siniestralidad elevada.
- Otras características, si aportan información relevante.

## Etapa 2: Construcción de conglomerados
- Analizar distribuciones, escalas y correlaciones de las nuevas características.
- Aplicar y comparar los métodos de agrupación.
- Buscar grupos homogéneos e interpretables, no necesariamente estables todavía.

## Etapa 3: Estabilidad temporal
- Construir ventanas móviles de cuatro años.
- Calcular las mismas características y repetir el agrupamiento en cada ventana.
- Evaluar ARI, cambios de pertenencia y permanencia de los segmentos.
- Comparar también los periodos independientes 2015–2018 y 2019–2022.

## Etapa 4: Confiabilidad actuarial
- Identificar segmentos con primas pequeñas, experiencia limitada o pérdidas extraordinarias.
- Evaluar cómo influyen los factores extremos en los conglomerados.
- Verificar si contamos con información suficiente para aplicar credibilidad actuarial.
- Considerar Bühlmann–Straub como análisis complementario de sensibilidad, si se justifican sus supuestos.

## Etapa 5: Selección final de conglomerados

**Criterios de evaluación:**
- Homogeneidad.
- Interpretabilidad.
- Robustez.
- Estabilidad temporal.
- Confiabilidad actuarial.

**Objetivo:** seleccionar y justificar los conglomerados más adecuados, reconociendo sus limitaciones.