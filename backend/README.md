# Backend (FastAPI) — despliegue en Railway

Este backend provee un streaming MJPEG en `/video_feed` usando OpenCV + MediaPipe.

Notas importantes antes de desplegar
- Los servicios cloud (Railway, Heroku, etc.) NO tienen acceso a tu cámara local.
  - Por defecto la app intentaba abrir la cámara del servidor (índice 0). Para evitar errores al iniciar en Railway, ahora la fuente de video está controlada por la variable de entorno `CAMERA_SOURCE`.

Configuración de `CAMERA_SOURCE`
- `CAMERA_SOURCE=none` (valor por defecto): la ruta `/video_feed` devolverá una imagen JPEG que indica que no hay fuente configurada.
- `CAMERA_SOURCE=0` (u otro entero): abrirá la cámara de ese índice en el servidor (solo útil si el servidor tiene cámara).
- `CAMERA_SOURCE=file:/path/to/file.mp4`: usará ese archivo de video como fuente (útil para demos o pruebas en cloud).

Archivo Procfile
- Se incluyó `Procfile` con la línea:

  web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

  Railway usará esto para iniciar el servidor.

Dependencias
- Revisar `requirements.txt`. Railway instalará esas dependencias automáticamente.

Pasos para desplegar en Railway
1. Subir este repositorio a GitHub (o conectar el repo a Railway directamente).
2. En Railway, crear un nuevo proyecto y seleccionar el repositorio.
3. Configurar la variable de entorno `CAMERA_SOURCE` si quieres usar un archivo de video:
   - Ejemplo: `file:/home/railway/app/sample.mp4` (sube el archivo al repo) o `none` para desactivar.
4. Desplegar. La URL pública servirá `/video_feed`.

Consideraciones
- Si quieres usar la cámara del cliente (navegador) para enviar video al backend, la arquitectura deberá cambiar: lo habitual es capturar en el frontend y enviarlo al servidor por WebRTC o WebSockets — eso requiere más cambios en la app.

