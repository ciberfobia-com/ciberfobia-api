# Instalación en Digital Ocean

Esta guía te muestra cómo desplegar la API de Ciberfobia en la App Platform de Digital Ocean.

## Requisitos previos

- Una cuenta en Digital Ocean ([Regístrate aquí](https://www.digitalocean.com/))
- Familiaridad básica con App Platform de Digital Ocean
- Una tarjeta de crédito/débito para la facturación (solo se cobra lo que uses)

## Paso 1: Crear un nuevo proyecto

1. Inicia sesión en tu cuenta de Digital Ocean  
2. Crea un nuevo proyecto o selecciona uno existente  
3. Esto organizará tus recursos para la API de Ciberfobia  

## Paso 2: Crear un Space en Digital Ocean

Necesitas crear un Space (almacenamiento de objetos de Digital Ocean) para que la API almacene los archivos procesados:

1. En el panel de Digital Ocean, entra en **Spaces Object Storage**  
2. Haz clic en **Create a Space**  
3. Selecciona una región (ej. New York)  
4. Pon un nombre al bucket (ej. `ciberfobia-bucket`)  
5. Selecciona tu proyecto  
6. Haz clic en **Create Space**  

## Paso 3: Generar claves de API para tu Space

1. Desde tu nuevo Space, ve a **Settings**  
2. Haz clic en **Create Access Key**  
3. Selecciona **Full Access**  
4. Ponle un nombre a la clave (ej. `ciberfobia-key`)  
5. Haz clic en **Create Access Key**  
6. **IMPORTANTE**: Guarda tanto la Access Key como la Secret Key – solo se muestran una vez  
7. Copia también la URL (endpoint) del Space para usar en el siguiente paso  

## Paso 4: Desplegar la aplicación

1. En el panel de Digital Ocean, haz clic en **Create** y selecciona **App**  
2. Elige **Container Image** como fuente de despliegue  
3. Selecciona **Docker Hub** como repositorio  
4. Introduce `ciberfobia/ciberfobia-api` como nombre de la imagen  
5. Introduce `latest` como tag  
6. Haz clic en **Next**  
7. Si es necesario, edita el nombre para eliminar guiones extra (Digital Ocean puede mostrar error con nombres largos)  
8. Selecciona **Web Service** como tipo de servicio  

## Paso 5: Configurar recursos

1. Selecciona un plan con recursos adecuados:  
   - Para pruebas, una instancia de $50/mes rinde bien  
   - Para cargas menores, elige una instancia más pequeña  
   - Nota: solo se cobra por el tiempo que el servidor está en ejecución  
2. Configura Containers en 1  
3. Cierra el diálogo de selección de recursos  

## Paso 6: Configurar variables de entorno

Añade estas variables exactamente como se muestran (ojo con guiones bajos/medios y sin espacios al inicio o final):

1. `API_KEY`: Tu clave de API (ej. `test123` para pruebas – cambia en producción)  
2. `S3_ENDPOINT_URL`: La URL de tu Space (del Paso 3)  
3. `S3_ACCESS_KEY`: La Access Key del Paso 3  
4. `S3_SECRET_KEY`: La Secret Key del Paso 3  
5. `S3_BUCKET_NAME`: El nombre del bucket (ej. `ciberfobia-bucket`)  
6. `S3_REGION`: El código de región del Space (ej. `NYC3` para New York)  

## Paso 7: Finalizar y desplegar

1. En Deployment Region, selecciona una región cercana a ti (ej. San Francisco)  
2. Usa el nombre por defecto de la app o uno personalizado  
3. Haz clic en **Create Resource**  
4. Espera a que el despliegue termine (puede tardar unos minutos)  
   - Puede que necesites refrescar la página para ver actualizaciones  

## Paso 8: Probar tu despliegue

### Con Postman

1. Regístrate o inicia sesión en [Postman](https://www.postman.com/)  
2. Importa la [colección Postman de Ciberfobia](https://bit.ly/49Gkh61)  
3. Haz fork de la colección a tu workspace  
4. Crea un nuevo entorno:  
   - Nómbralo "Digital Ocean" o similar  
   - Añade la variable `x-api-key` con el valor de tu `API_KEY` (ej. `test123`)  
   - Añade la variable `base_url` con la URL de tu app (mostrada en el panel de Digital Ocean)  
   - Guarda el entorno  
5. En la colección, ve al endpoint `toolkit/authenticate` y haz clic en Send  
6. Si recibes una respuesta correcta, el despliegue funciona  
7. Luego prueba el endpoint `toolkit/test` para verificar toda la funcionalidad  

## Monitorización y gestión

- **Overview**: ver información básica de la app  
- **Insights**: monitorizar uso de CPU y memoria  
- **Runtime Logs**: ver logs de llamadas API y actividad del servidor  
- **Console**: acceder a la línea de comandos del servidor (rara vez necesario)  
- **Settings**: modificar la configuración de la app  

## Próximos pasos

Ahora que has desplegado con éxito la API de Ciberfobia, puedes:  
- Explorar todos los endpoints disponibles en la colección Postman  
- Integrar la API en tus aplicaciones  
- Proteger tu clave de API con un valor más complejo  
- Escalar los recursos hacia arriba o abajo según tus necesidades  

Recuerda: Digital Ocean cobra por uso, así que puedes eliminar la app cuando no la necesites para ahorrar costes.