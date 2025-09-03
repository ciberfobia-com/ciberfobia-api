# Añadir Nuevas Rutas

Este documento explica cómo añadir nuevas rutas a la aplicación usando el sistema de registro dinámico de rutas.

## Descripción General

La aplicación utiliza ahora un sistema de registro dinámico que descubre y registra automáticamente todos los *blueprints* de Flask en el directorio `routes`. Ya no es necesario importarlos manualmente en `app.py`.

## Cómo Añadir una Nueva Ruta

1. **Crear un nuevo archivo de ruta**

   Crea un archivo Python en la ubicación adecuada dentro de `routes`. Para un endpoint v1, normalmente dentro de `routes/v1/` según la funcionalidad.

   Ejemplo:

   ```
   routes/v1/email/send_email.py
   ```

2. **Definir el Blueprint**

   Dentro del archivo, define un *blueprint* con un nombre único siguiendo la convención:

   ```python
   # routes/v1/email/send_email.py
   from flask import Blueprint, request
   from services.authentication import authenticate
   from app_utils import queue_task_wrapper

   v1_email_send_bp = Blueprint('v1_email_send', __name__)

   @v1_email_send_bp.route('/v1/email/send', methods=['POST'])
   @authenticate
   @queue_task_wrapper(bypass_queue=False)
   def send_email(job_id, data):
       """
       Enviar un correo electrónico
       
       Args:
           job_id (str): ID de la tarea asignado por queue_task_wrapper
           data (dict): Datos de la petición con la información del email
       
       Returns:
           Tuple (response_data, endpoint_string, status_code)
       """
       endpoint = "/v1/email/send"
       return {"message": "Email enviado"}, endpoint, 200
   ```

3. **Listo**

   No es necesario modificar `app.py`. El *blueprint* será detectado y registrado automáticamente al iniciar la aplicación.

## Convenciones de Nombres

* **Blueprints**: `{version}_{categoria}_{accion}_bp`
  Ejemplo: `v1_email_send_bp`

* **Rutas**: `/{version}/{categoria}/{accion}`
  Ejemplo: `/v1/email/send`

* **Archivos**: En directorios que reflejen la estructura de la ruta
  Ejemplo: `routes/v1/email/send_email.py`

## Probar la Ruta

Tras añadirla, reinicia la aplicación y el nuevo endpoint estará disponible.

## Solución de Problemas

Si la ruta no se registra:

1. Revisa los logs por errores de importación
2. Comprueba que el *blueprint* está definido a nivel de módulo
3. Verifica que el nombre sigue la convención
4. Asegúrate de que el archivo está en el directorio correcto bajo `routes/`