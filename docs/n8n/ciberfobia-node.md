# n8n-nodes-ciberfobia-api

Nodo para integrar la **Ciberfobia API** directamente en tus flujos de trabajo en **n8n**.

---

## 📦 Instalación

1. Abre tu instancia de **n8n**.  
2. Ve a **Settings → Community Nodes**.  
3. Pulsa **Install** e introduce el nombre del paquete:

n8n-nodes-ciberfobia-api

4. Haz clic en **Install** y espera a que termine.  
5. Reinicia **n8n** si es necesario.

---

## 🔑 Configuración de credenciales

Al crear las credenciales para este nodo se requieren dos parámetros:  

- **Base URL** → la URL de tu despliegue de la API de Ciberfobia (ejemplo: `https://api.tudominio.com`).  
- **API Key** → la clave de autenticación que hayas configurado en tu entorno.  

Una vez guardadas, estas credenciales se usan en cualquier endpoint de la API.

---

## 📂 Endpoints disponibles

El nodo permite acceder a **todos los endpoints** definidos en la API de Ciberfobia, incluyendo:  

- `/toolkit/*`  
- `/ffmpeg/*`  
- `/code/*`  
- `/audio/*`  
- `/video/*`  
- `/image/*`  
- `/media/*`  
- `/s3/*`  
- y el resto de recursos expuestos en la API.  

---

## 🛠️ Ejemplo de uso

1. Crea un nuevo flujo en n8n.  
2. Añade el nodo **Ciberfobia API**.  
3. Configura la credencial con tu **Base URL** y tu **API Key**.  
4. Selecciona el recurso y la acción que quieras ejecutar (cualquier endpoint disponible).  
5. Ejecuta el nodo y revisa la respuesta.  

---

## 📖 Próximos pasos

- Explora la [documentación de la API de Ciberfobia](../README.md) para ver los endpoints soportados.  
- Combina este nodo con otros de n8n (Gmail, Google Drive, Airtable, etc.) para crear automatizaciones avanzadas.  
