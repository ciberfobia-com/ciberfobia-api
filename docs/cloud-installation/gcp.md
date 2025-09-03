# Instalación en Google Cloud Platform (GCP)

## 🎥 Instrucciones en video

Mira **[Instrucciones detalladas en video]('PROXIMAMENTE')** para configurar la API de Ciberfobia.

- Usa la **imagen de Docker**:

ciberfobia/ciberfobia-api:latest

### Recursos

- **Nodo Ciberfobia para n8n**: disponible en Community Nodes con la ID `n8n-nodes-ciberfobia-api`

---

## Requisitos previos

- Una cuenta en Google Cloud ([registro aquí](https://cloud.google.com/))  
- Los nuevos usuarios reciben $300 en créditos gratuitos  
- Conocimientos básicos de Cloud Run y Cloud Storage  
- Una terminal o editor de código  

---

## Paso 1: Crear un proyecto en Google Cloud
1. Inicia sesión en la [Consola de GCP](https://console.cloud.google.com/).  
2. Selecciona **New Project** desde **Project Selector**.  
3. Ponle un nombre (ej. `Ciberfobia Project`).  
4. Haz clic en **Create**.  

---

## Paso 2: Habilitar APIs necesarias
Activa:  
- **Cloud Storage API**  
- **Cloud Storage JSON API**  
- **Cloud Run API**

En la consola: **APIs & Services → Enable APIs and Services**, busca cada una y actívala.  

---

## Paso 3: Crear una Service Account
1. En la consola, ve a **IAM & Admin → Service Accounts**.  
2. Crea una nueva con nombre (ej. `Ciberfobia Service Account`).  
3. Asigna roles: **Storage Admin** y **Viewer**.  
4. Crea y descarga una clave en formato **JSON**.  

---

## Paso 4: Crear un bucket en Cloud Storage
1. Ve a **Storage → Buckets → + Create Bucket**.  
2. Pon un nombre único (ej. `ciberfobia-bucket`).  
3. Configura:  
   - Desactiva **Enforce public access prevention**  
   - **Access Control** en **Uniform**  
4. Da permisos de lectura pública añadiendo `allUsers` con rol **Storage Object Viewer**.  

---

## Paso 5: Desplegar en Cloud Run
1. Abre **Cloud Run** y crea un nuevo servicio.  
2. Elige despliegue desde Docker Hub con la imagen:  

ciberfobia/ciberfobia-api:latest

3. Permite invocaciones no autenticadas.  
4. Configura recursos: 16 GB RAM, 4 CPUs, Always Allocated.  
5. Escalado: mínimo `0`, máximo `5`.  
6. Usa **Second Generation**.  
7. Variables de entorno:  
   - `API_KEY` → tu clave API  
   - `GCP_BUCKET_NAME` → tu bucket  
   - `GCP_SA_CREDENTIALS` → contenido completo del JSON de la service account  
8. Configuración avanzada:  
   - Puerto `8080`  
   - Timeout `300s`  
   - Startup Boost habilitado  
9. Haz clic en **Create**.  

---

## Paso 6: Probar despliegue
1. Instala el nodo **Ciberfobia en n8n** (`n8n-nodes-ciberfobia-api`) para validar directamente en tus flujos.
2. Configura variables:  
   - `base_url` = URL de Cloud Run  
   - `x-api-key` = tu clave API  
3. Ejecuta peticiones de ejemplo.  

---

Con esto, la API de Ciberfobia quedará desplegada y lista para integrarse en Google Cloud Platform.