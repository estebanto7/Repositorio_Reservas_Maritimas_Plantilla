# Publicar en GitHub desde VS Code (primer repositorio)

## Método A: interfaz de VS Code

1. Descomprime esta carpeta y ábrela con **File > Open Folder**.
2. Copia tu notebook real a `notebooks/` (o adapta los notebooks guía). No subas bases originales sin autorización.
3. Abre **Source Control** (icono de ramificación) y pulsa **Initialize Repository**, si aún no existe uno.
4. Revisa los cambios; confirma que NO aparezcan `.xlsx`, `.env`, ni `.venv`.
5. Escribe un mensaje de commit: `Estructura inicial y documentación del proyecto` y pulsa **Commit**.
6. Pulsa **Publish Branch** / **Publish to GitHub**. Inicia sesión cuando VS Code lo solicite.
7. Elige repositorio privado al principio; después puedes cambiarlo si te autorizan compartir el contenido.
8. Abre GitHub y confirma que se ve `README.md`, carpetas, notebooks y archivos de código.

## Método B: terminal (si prefieres aprender Git)

Primero crea un repositorio vacío en GitHub (sin crear README en la web), luego desde la carpeta del proyecto:

```bash
git init
git add .
git status
git commit -m "Estructura inicial del análisis actuarial"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/Analisis-Reservas-Seguros-Maritimos.git
git push -u origin main
```

Sustituye `TU-USUARIO` por tu usuario real. Es posible que GitHub solicite autenticación mediante navegador o un gestor de credenciales.

## Mantenerlo actualizado

Después de terminar un apartado:

```bash
git add .
git commit -m "Analiza evolución de primas y comisiones"
git push
```

Revisa `git status` **antes** de cada commit. No publiques datos confidenciales ni tokens. Si por error se sube información sensible, borrarla en un commit nuevo no basta para eliminarla del historial.
