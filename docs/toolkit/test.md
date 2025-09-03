# Toolkit Test Endpoint

## 1. Descripción

El endpoint `/v1/toolkit/test` forma parte de la Toolkit API y sirve para comprobar la configuración básica de la API. Crea un archivo temporal, lo sube al almacenamiento en la nube y devuelve la URL del archivo. Es una prueba sencilla para confirmar que la API está correctamente configurada y que puede realizar operaciones básicas de archivos y almacenamiento.

## 2. Endpoint

* **URL Path:** `/v1/toolkit/test`
* **HTTP Method:** `GET`

## 3. Request

### Headers

* `x-api-key` (**requerido**): clave API para autenticación.

### Body

No requiere parámetros en el cuerpo de la petición.

### Ejemplo

```bash
curl -X GET \
  https://your-api-url.com/v1/toolkit/test \
  -H 'x-api-key: your-api-key'
```

## 4. Response

### Éxito (200 OK)

```json
{
  "endpoint": "/v1/toolkit/test",
  "code": 200,
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://cloud-storage.com/success.txt",
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 0.123,
  "queue_time": 0.0,
  "total_time": 0.123,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Error (401 Unauthorized)

```json
{
  "code": 401,
  "message": "Unauthorized: Invalid or missing API key"
}
```

### Error (500 Internal Server Error)

```json
{
  "code": 500,
  "message": "An error occurred while processing the request"
}
```

## 5. Manejo de Errores

* API key inválida o ausente → **401 Unauthorized**.
* Error interno en la creación o subida del archivo → **500 Internal Server Error**.

## 6. Notas de Uso

* Es un endpoint de prueba, sin parámetros especiales.
* Útil para verificar la configuración y el funcionamiento básico de la API.

## 7. Problemas Comunes

* API key incorrecta o ausente.
* Fallos en la creación del archivo temporal o en la subida a la nube.

## 8. Buenas Prácticas

* Usar este endpoint en la fase de configuración inicial de la API.
* Ejecutar pruebas periódicas con este endpoint para detectar cambios o problemas en la configuración.