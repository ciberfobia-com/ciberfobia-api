# Ciberfobia-api

¿Cansado de gastar miles de dólares en suscripciones de API para automatizar tus procesos? 

¿Qué tal si existiera una alternativa 100% GRATUITA?  

**Ciberfobia-api** es una API de procesamiento multimedia, construida en Python con Flask, que te permite convertir archivos de audio, generar transcripciones, traducir contenido, añadir subtítulos a videos y mucho más.

---

## 🚀 ¿Qué puede hacer Ciberfobia-api?

La API realiza diversas tareas relacionadas con la manipulación de medios, siempre con una robusta validación de datos y documentación detallada para facilitar su integración.

### 🎮 Manipulación Avanzada de Medios

#### 1. `/v1/ffmpeg/compose`
- **Descripción**: Permite componer y manipular archivos multimedia utilizando FFmpeg, soportando operaciones complejas como transcodificación, concatenación y filtrado.
- **Documentación**: [FFmpeg Compose Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/ffmpeg/ffmpeg_compose.md)

---

### 📹 Procesamiento de Video

#### 2. `/v1/video/caption`
- **Descripción**: Añade subtítulos a un video, con opciones para configurar fuente, posición y estilo. Soporta detección automática del idioma y reemplazos personalizados.
- **Documentación**: [Video Caption Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/video/caption_video.md)

#### 3. `/v1/video/concatenate`
- **Descripción**: Combina múltiples archivos de video en uno solo, respetando el orden especificado, y sube el resultado al almacenamiento en la nube.
- **Documentación**: [Video Concatenate Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/video/concatenate.md)

---

### 💻 Ejecución de Código

#### 4. `/v1/code/execute/python`
- **Descripción**: Ejecuta código Python en el servidor en un entorno controlado, ideal para scripting, prototipos o ejecución dinámica de scripts.
- **Documentación**: [Execute Python Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/code/execute/execute_python.md)

---

### 🖼️ Procesamiento de Imágenes

#### 5. `/v1/image/transform/video`
- **Descripción**: Convierte una imagen en un archivo de video, con opciones configurables como duración, velocidad de fotogramas y efectos de zoom, perfecto para crear presentaciones.
- **Documentación**: [Image to Video Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/image/transform/image_to_video.md)

---

### 🎵 Transformación de Medios

#### 6. `/v1/media/transform/mp3`
- **Descripción**: Transforma archivos multimedia a formato MP3, con opciones avanzadas para configurar la tasa de bits y la frecuencia de muestreo.
- **Documentación**: [Media Transform to MP3 Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/media/transform/media_to_mp3.md)

#### 7. `/v1/media/transcribe`
- **Descripción**: Transcribe archivos de audio a texto usando procesamiento avanzado de reconocimiento de voz, soportando varios idiomas y formatos.
- **Documentación**: [Audio Transcribe Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/media/media_transcribe.md)

---

### ⚖️ Funciones Básicas

#### 8. `/v1/toolkit/test`
- **Descripción**: Un endpoint básico para verificar la disponibilidad y el correcto funcionamiento de la API. Útil para pruebas iniciales.
- **Documentación**: [Test Endpoint Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/toolkit/test.md)

#### 9. `/v1/toolkit/authenticate`
- **Descripción**: Verifica la API key proporcionada y autentica al usuario, retornando un mensaje de éxito si la autenticación es correcta.
- **Documentación**: [Authenticate Endpoint Documentation](https://github.com/internetesfera/ciberfobia-api/blob/main/docs/toolkit/authenticate.md)

---

## 🐳 Construcción y Ejecución con Docker

### Construir la Imagen Docker

```bash
docker build -t ciberfobia-api .
```

### Variables de Entorno Generales

#### `API_KEY`
- **Propósito**: Clave para la autenticación de la API.
- **Requerida**: Sí, es obligatoria.

---

### Variables de Entorno para Google Cloud Platform (GCP)

#### `GCP_SA_CREDENTIALS`
- **Propósito**: Credenciales en formato JSON de la cuenta de servicio de GCP.
- **Requerida**: Obligatoria si usas almacenamiento GCP.

#### `GCP_BUCKET_NAME`
- **Propósito**: Nombre del bucket de almacenamiento en GCP.
- **Requerida**: Obligatoria si usas almacenamiento GCP.

---

### Variables de Entorno para Almacenamiento Compatible con S3 (ej. DigitalOcean Spaces)

#### `S3_ENDPOINT_URL`
- **Propósito**: URL del endpoint del servicio S3.
- **Requerida**: Obligatoria si usas un servicio S3.

#### `S3_ACCESS_KEY`
- **Propósito**: Clave de acceso para el servicio S3.
- **Requerida**: Obligatoria si usas un servicio S3.

#### `S3_SECRET_KEY`
- **Propósito**: Clave secreta para el servicio S3.
- **Requerida**: Obligatoria si usas un servicio S3.

---

### Ejecución del Contenedor Docker

```bash
docker run -d -p 8080:8080 \
  -e API_KEY=tu_api_key \
  -e GCP_SA_CREDENTIALS='{"tu":"json_de_cuenta_de_servicio"}' \
  -e GCP_BUCKET_NAME=nombre_de_tu_bucket \
  ciberfobia-api
```

---

## ☁️ Instalación en Google Cloud Platform (GCP)

### 📹 Instrucciones en Video

Mira video (proximamente) para configurar Ciberfobia-api en GCP.

- Utiliza la imagen Docker:
  ```
  internetesfera/ciberfobia-api:latest
  ```

### Recursos adicionales

- **Plantilla Postman** proximamente
- **Ciberfobia-api GPT** proximamente

---

## 📋 Requisitos Previos

- Una cuenta de Google Cloud. [Regístrate aquí]([https://cloud.google.com/](https://cloud.google.com/free)) si aún no tienes una.
  - Los nuevos usuarios reciben $300 en créditos gratuitos.
- Conocimientos básicos de servicios GCP como Cloud Run y Cloud Storage.
- Terminal o editor de código para gestionar archivos.

---

## 🛠️ Pasos para Desplegar en GCP

### Paso 1: Crear un Proyecto en Google Cloud
1. Accede a la [Consola de GCP](https://console.cloud.google.com/).
2. Haz clic en el **Selector de Proyectos** y elige **Nuevo Proyecto**.
3. Ingresa un nombre para el proyecto, por ejemplo, `Ciberfobia-api`.
4. Haz clic en **Crear**.

---

### Paso 2: Habilitar APIs Requeridas
Habilita las siguientes APIs:
- Cloud Storage API
- Cloud Storage JSON API
- Cloud Run Admin API

**Cómo Habilitar:**
1. En la Consola de GCP, ve a **APIs & Services** > **Habilitar APIs y Servicios**.
2. Busca cada API, haz clic en ella y selecciona **Habilitar**.

---

### Paso 3: Crear una Cuenta de Servicio
1. Ve a **IAM & Admin** > **Cuentas de Servicio**.
2. Haz clic en **+ Crear Cuenta de Servicio**.
   - Ingresa un nombre, por ejemplo, `Cuenta de Servicio Ciberfobia`.
3. Asigna los roles:
   - **Storage Admin** (Administrador de objetos de Storage).
   - **Viewer** (Visualizador).
4. Haz clic en **Listo**.
5. En los detalles de la cuenta, en la pestaña **Claves**, haz clic en **Agregar Clave** > **Crear Nueva Clave** (formato JSON). Descarga y guarda el archivo de forma segura (lo usaremos después).

---

### Paso 4: Crear un Bucket en Cloud Storage
1. Ve a **Storage** > **Buckets**.
2. Haz clic en **+ Crear Bucket**.
   - Elige un nombre único, por ejemplo, `ciberfobia-bucket`.
   - Configura los ajustes, asegurándote de:
     - Desmarcar **Forzar prevención de acceso público**.
     - Configurar **Control de Acceso** como **Uniforme**.
3. Haz clic en **Crear**.
4. En los permisos del bucket, agrega **allUsers** con el rol **Storage Object Viewer** (Visualizador de objetos de Storage).

---

### Paso 5: Desplegar en Cloud Run
1. Accede al servicio **Cloud Run** en la Consola de GCP.
2. Haz clic en **Crear Servicio** y selecciona **Desplegar una revisión desde Docker Hub** utilizando la imagen:
   ```
   internetesfera/ciberfobia-api:latest
   ```
3. Permite invocaciones no autenticadas.
4. Configura la asignación de recursos:
   - Memoria: 16 GB
   - CPU: 4 CPUs (siempre asignadas)
5. Ajusta la escalabilidad:
   - Instancias Mínimas: 0
   - Instancias Máximas: 5 (ajustable según carga)
6. Selecciona **Segunda Generación** en la versión de plataforma.
7. Agrega las variables de entorno:
   - `API_KEY`: Tu clave API (ej. `Test123`)
   - `GCP_BUCKET_NAME`: Nombre de tu bucket de Cloud Storage
   - `GCP_SA_CREDENTIALS`: Contenido JSON completo de la clave de la cuenta de servicio
8. Configura ajustes avanzados:
   - Puerto del contenedor: 8080
   - Tiempo de espera: 300 segundos
   - Activa **Startup Boost** para mejorar el rendimiento en el arranque.
9. Verifica la configuración y haz clic en **Crear**.

---

### Paso 6: Probar el Despliegue (proximamente)
1. Instala **Postman**.
2. Importa los ejemplos de peticiones de la API.
3. Configura en Postman las variables:
   - `base_url`: URL de tu servicio en Cloud Run.
   - `x-api-key`: Tu API key configurada.
4. Ejecuta las peticiones de ejemplo para verificar el funcionamiento.
5. Consulta **Ciberfobia-api GPT** para más información.

---

## 🤝 Contribuir a Ciberfobia-api

¡Tus contribuciones son bienvenidas! Para aportar al proyecto:
1. Haz un fork del repositorio.
2. Crea una rama nueva para tus cambios.
3. Realiza tus modificaciones.
4. Envía un pull request a la rama "build".

**Proceso de Pull Request:**
- Asegúrate de eliminar dependencias o archivos generados antes de finalizar el build.
- Actualiza el README.md con los cambios realizados: nuevas variables, puertos expuestos, ubicaciones útiles y parámetros del contenedor.

¡Gracias por colaborar!

---

## 📜 Soporte

Si necesitas ayuda, obtén cursos, únete a la comunidad y participa en llamadas diarias.  
Únete a la **[Comunidad Ciberfobia](https://www.skool.com/ciberfobia)** (proximamente).

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

