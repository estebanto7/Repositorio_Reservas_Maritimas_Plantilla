# Origen y gestión de datos

**No subas datos originales sin autorización.** Git ignora los `.xlsx` y otras tablas.

Coloca de forma local en `raw/`:

- `2026 BASE RESERVAS(1).xlsx`, con hojas históricas `EMISION` y `SINIESTRALIDAD`.
- `EMISION 2025.xlsx`, con información detallada de vigencias para la RRC.

Los nombres son orientativos; comprueba que coincidan con los que tienes en tu equipo. Los datos limpios y transformados deben guardarse en `processed/`. **No edites los originales**, conserva una copia de respaldo y documenta fechas, filtros y unidades.

Los tests utilizan datos sintéticos; no requieren compartir archivos reales.
