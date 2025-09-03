<img src="https://raw.githubusercontent.com/ciberfobia-com/ciberfobia-api/main/assets/ciberfobia-logo.png" alt="Logo Original Ciberfobia" width="200"/>

# Ciberfobia API

¿Cansado de gastar miles de euros en suscripciones de APIs para soportar todas tus automatizaciones? ¿Y si existiera una alternativa gratuita?

La **Ciberfobia API**, 100% GRATIS, procesa distintos tipos de medios. Está construida en Python usando Flask.

## ¿Qué puede hacer?

La API convierte archivos de audio. Genera transcripciones. Traduce contenido entre idiomas. Añade subtítulos a vídeos. Puede realizar procesamiento avanzado de medios para creación de contenido. También gestiona archivos en múltiples servicios en la nube como Google Drive, Amazon S3, Google Cloud Storage y Dropbox.

Se puede desplegar de varias formas: funciona con Docker, en Google Cloud Platform, en Digital Ocean o en cualquier sistema que soporte Docker.

Reemplaza fácilmente servicios como ChatGPT Whisper, Cloud Convert, Createomate, JSON2Video, PDF(dot)co, Placid y OCodeKit.

## 👥 Comunidad Ciberfobia

¿Quieres ayuda? Únete a la comunidad y obtén soporte técnico dedicado.

La **única comunidad** donde aprendes a aprovechar la IA, la automatización y el contenido para hacer crecer tu negocio (y simplificarlo).

¿Para quién es esto?

* Coaches y consultores
* Agencias de automatización con IA
* Agencias de contenidos y SMMA
* Fundadores de startups SaaS

Accede a cursos, comunidad, soporte, llamadas diarias y más.

Únete a la **[Comunidad Ciberfobia](https://ciberfobia.com/whatsapp)** hoy mismo.

---

## Endpoints de la API

Cada endpoint incluye validación robusta de payloads y documentación detallada para facilitar la integración.

### Audio

* **[`/v1/audio/concatenate`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/audio/concatenate.md)**

  * Combina varios archivos de audio en uno solo.

### Code

* **[`/v1/code/execute/python`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/code/execute/execute_python.md)**

  * Ejecuta código Python de forma remota y devuelve el resultado.

### FFmpeg

* **[`/v1/ffmpeg/compose`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/ffmpeg/ffmpeg_compose.md)**

  * Interfaz flexible de FFmpeg para procesamiento complejo de medios.

### Imagen

* **[`/v1/image/convert/video`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/image/convert/image_to_video.md)**

  * Convierte una imagen estática en vídeo con duración y efectos de zoom.

* **[`/v1/image/screenshot/webpage`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/image/screenshot_webpage.md)**

  * Captura pantallazos de páginas web con opciones avanzadas como viewport, emulación de dispositivos o inyección de HTML/CSS/JS.

### Media

* **[`/v1/media/convert`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/convert/media_convert.md)**

  * Convierte archivos multimedia de un formato a otro con opciones de códecs.

* **[`/v1/media/convert/mp3`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/convert/media_to_mp3.md)**

  * Convierte distintos formatos a MP3.

* **[`/v1/BETA/media/download`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/download.md)**

  * Descarga contenido multimedia online con yt-dlp.

* **[`/v1/media/feedback`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/feedback.md)**

  * Interfaz web para recoger y mostrar feedback sobre medios.

* **[`/v1/media/transcribe`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/media_transcribe.md)**

  * Transcribe o traduce contenido de audio/vídeo desde una URL.

* **[`/v1/media/silence`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/silence.md)**

  * Detecta intervalos de silencio en un archivo multimedia.

* **[`/v1/media/metadata`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/media/metadata.md)**

  * Extrae metadatos completos de archivos multimedia (formatos, códecs, resolución, bitrates).

### S3

* **[`/v1/s3/upload`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/s3/upload.md)**

  * Sube archivos a S3 directamente desde una URL.

### Toolkit

* **[`/v1/toolkit/authenticate`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/toolkit/authenticate.md)**

  * Autenticación básica para validar API keys.

* **[`/v1/toolkit/test`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/toolkit/test.md)**

  * Verifica que la Ciberfobia API está correctamente instalada.

* **[`/v1/toolkit/job/status`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/toolkit/job_status.md)**

  * Obtiene el estado de un trabajo por su ID.

* **[`/v1/toolkit/jobs/status`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/toolkit/jobs_status.md)**

  * Obtiene el estado de todos los trabajos en un rango temporal.

### Vídeo

* **[`/v1/video/caption`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/caption_video.md)**

  * Añade subtítulos personalizables a vídeos.

* **[`/v1/video/concatenate`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/concatenate.md)**

  * Combina varios vídeos en uno solo.

* **[`/v1/video/thumbnail`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/thumbnail.md)**

  * Extrae un fotograma como miniatura de un vídeo.

* **[`/v1/video/cut`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/cut.md)**

  * Corta segmentos de un vídeo con opciones de codificación.

* **[`/v1/video/split`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/split.md)**

  * Divide un vídeo en segmentos según tiempos de inicio y fin.

* **[`/v1/video/trim`](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/video/trim.md)**

  * Recorta un vídeo manteniendo solo entre un inicio y un fin.

---

## Docker Build y Run

### Construir la imagen Docker

```bash
docker build -t ciberfobia/ciberfobia-api:latest .
```

### Variables de entorno principales

#### `API_KEY`

* **Propósito**: Usada para autenticar en la API.
* **Obligatorio**: Sí.

---

### Variables para almacenamiento S3

#### `S3_ENDPOINT_URL`

* URL del servicio S3-compatible.
* Obligatorio si usas S3.

#### `S3_ACCESS_KEY`

* Access key del servicio S3.
* Obligatorio si usas S3.

#### `S3_SECRET_KEY`

* Secret key del servicio S3.
* Obligatorio si usas S3.

#### `S3_BUCKET_NAME`

* Nombre del bucket.
* Obligatorio si usas S3.

#### `S3_REGION`

* Región del bucket.
* Obligatorio si usas S3 (puede ser `"None"` en algunos proveedores).

---

### Variables Google Cloud Storage (GCP)

#### `GCP_SA_CREDENTIALS`

* Credenciales JSON de la Service Account de GCP.
* Obligatorio si usas GCP.

#### `GCP_BUCKET_NAME`

* Nombre del bucket en GCP.
* Obligatorio si usas GCP.

---

### Variables de rendimiento

#### `MAX_QUEUE_LENGTH`

* Máximo de tareas en la cola.
* Por defecto: 0 (ilimitado).

#### `GUNICORN_WORKERS`

* Número de workers de Gunicorn.
* Por defecto: núcleos de CPU + 1.

#### `GUNICORN_TIMEOUT`

* Timeout en segundos.
* Por defecto: 30.

---

### Configuración de almacenamiento local

#### `LOCAL_STORAGE_PATH`

* Carpeta temporal para almacenamiento durante el procesado.
* Por defecto: `/tmp`.

---

### Ejecutar el contenedor Docker

```bash
docker run -d -p 8080:8080 \
  -e API_KEY=tu_api_key \
  -e LOCAL_STORAGE_PATH=/tmp \
  -e MAX_QUEUE_LENGTH=10 \
  -e GUNICORN_WORKERS=4 \
  -e GUNICORN_TIMEOUT=300 \
  ciberfobia/ciberfobia-api:latest
```

---

## Guías de instalación

### Digital Ocean

* [Guía Digital Ocean](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/cloud-installation/do.md)

### Google Cloud Run

* [Guía Google Cloud Run](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docs/cloud-installation/gcp.md)

### Docker general

* [Guía Docker Compose](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docker-compose.md)

### Desarrollo local con MinIO y n8n

* [Guía local MinIO + n8n](https://github.com/ciberfobia-com/ciberfobia-api/blob/main/docker-compose.local.minio.n8n.md)

---

## Tests de la API

### Llamadas HTTP directas

1. Configura la variable `x-api-key`.  
2. Haz peticiones al `base_url` con `curl`, POSTMAN u otra herramienta HTTP:  

   ```bash
   curl -X POST "https://TU_BASE_URL/v1/toolkit/test" \
   -H "x-api-key: TU_API_KEY" \
   -H "Content-Type: application/json" \
   -d '{}'
   ````

### Nodo de n8n

1. Abre tu instancia de **n8n**.
2. Ve a **Settings → Community Nodes**.
3. Instala el paquete:

   ```
   n8n-nodes-ciberfobia-api
   ```
4. Arrastra el nodo a un workflow y selecciona el endpoint que quieras probar.

---

## Contribuciones a la Ciberfobia API

1. Haz fork del repo
2. Crea una rama
3. Haz cambios
4. PR a `build`

Guía de rutas: [docs/adding\_routes.md](docs/adding_routes.md)

---

## Licencia

Este proyecto está bajo licencia [GNU GPL-2.0](LICENSE).
