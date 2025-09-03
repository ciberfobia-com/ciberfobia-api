# Get All Jobs Status

## 1. Descripción

El endpoint `/v1/toolkit/jobs/status` forma parte de la Toolkit API y permite obtener el estado de todos los trabajos dentro de un rango de tiempo determinado. Es útil para monitorizar y gestionar las tareas enviadas al sistema. Pertenece al *blueprint* `v1_toolkit_jobs_status_bp` registrado en `app.py`.

## 2. Endpoint

* **URL Path:** `/v1/toolkit/jobs/status`
* **HTTP Method:** `POST`

## 3. Request

### Headers

* `x-api-key` (**requerido**): clave API para autenticación.

### Body Parameters

* `since_seconds` (**opcional**, número): segundos hacia atrás para consultar trabajos.

  * Valor por defecto: **600** (10 minutos).
  * El cuerpo es opcional; si no se envía, se usa el valor por defecto.

### Ejemplos

```json
{
  "since_seconds": 3600
}
```

```bash
curl -X POST \
     -H "x-api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     http://your-api-url/v1/toolkit/jobs/status
```

```bash
curl -X POST \
     -H "x-api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"since_seconds": 3600}' \
     http://your-api-url/v1/toolkit/jobs/status
```

## 4. Response

### Éxito (200 OK)

```json
{
  "code": 200,
  "id": null,
  "job_id": "job_id_value",
  "response": {
    "job_id_1": "job_status_1",
    "job_id_2": "job_status_2"
  },
  "message": "success",
  "run_time": 0.123,
  "queue_time": 0,
  "total_time": 0.123,
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Error (404 Not Found)

```json
{
  "code": 404,
  "id": null,
  "job_id": "job_id_value",
  "response": null,
  "message": "Jobs directory not found",
  "run_time": 0.123,
  "queue_time": 0,
  "total_time": 0.123,
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Error (500 Internal Server Error)

```json
{
  "code": 500,
  "id": null,
  "job_id": "job_id_value",
  "response": null,
  "message": "Failed to retrieve job statuses: Error message",
  "run_time": 0.123,
  "queue_time": 0,
  "total_time": 0.123,
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

* API key inválida/faltante → **401 Unauthorized**.
* Directorio de trabajos no encontrado → **404 Not Found**.
* Error en la recuperación de estados → **500 Internal Server Error**.
* Cola llena → **429 Too Many Requests**.

## 6. Notas de Uso

* Permite monitorizar trabajos largos o en cola.
* `since_seconds` ajusta el rango temporal de consulta.

## 7. Problemas Comunes

* Usar API key inválida.
* Directorio de trabajos inexistente.
* Excepciones al recuperar estados.

## 8. Buenas Prácticas

* Incluir siempre API key válida.
* Monitorizar estados regularmente.
* Ajustar `since_seconds` según necesidades.
* Implementar logs y manejo de errores en el cliente.
