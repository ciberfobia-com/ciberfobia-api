# Job Status Endpoint

## 1. Descripción

El endpoint `/v1/toolkit/job/status` pertenece a la Toolkit API y permite consultar el estado de un trabajo específico. Se utiliza como utilidad de monitorización y gestión de tareas enviadas a los distintos endpoints de procesamiento multimedia.

## 2. Endpoint

* **URL Path:** `/v1/toolkit/job/status`
* **HTTP Method:** `POST`

## 3. Request

### Headers

* `x-api-key` (**requerido**): clave API para autenticación.

### Body Parameters

* `job_id` (**string, requerido**): identificador único del trabajo.

#### JSON Schema

```python
{
    "type": "object",
    "properties": {
        "job_id": {"type": "string"}
    },
    "required": ["job_id"]
}
```

### Ejemplo

```json
{
  "job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7"
}
```

```bash
curl -X POST \
     -H "x-api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7"}' \
     http://your-api-endpoint/v1/toolkit/job/status
```

## 4. Response

### Éxito (200 OK)

```json
{
  "endpoint": "/v1/toolkit/job/status",
  "code": 200,
  "id": null,
  "job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7",
  "response": {
    "job_status": "done",
    "job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7",
    "queue_id": 140368864456064,
    "process_id": 123456,
    "response": {
      "endpoint": "/v1/media/transcribe",
      "code": 200,
      "id": "transcribe_job_123",
      "job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7",
      "response": "Transcription completed successfully.",
      "message": "success",
      "pid": 123456,
      "queue_id": 140368864456064,
      "run_time": 5.234,
      "queue_time": 1.123,
      "total_time": 6.357,
      "queue_length": 0,
      "build_number": "1.0.0"
    }
  },
  "message": "success",
  "pid": 123456,
  "queue_id": 140368864456064,
  "run_time": 0.001,
  "queue_time": 0.0,
  "total_time": 0.001,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Error (404 Not Found)

```json
{
  "error": "Job not found",
  "job_id": "e6d7f3c0-9c9f-4b8a-b7c3-f0e3c9f6b9d7"
}
```

### Error (500 Internal Server Error)

```json
{
  "error": "Failed to retrieve job status: <error_message>",
  "code": 500
}
```

## 5. Manejo de Errores

* Parámetros inválidos/faltantes → **400 Bad Request**.
* `job_id` inexistente → **404 Not Found**.
* Error inesperado → **500 Internal Server Error**.
* Cola llena → **429 Too Many Requests**.

## 6. Notas de Uso

* Requiere API key válida.
* `job_id` debe ser UUID válido de un trabajo existente.
* Solo consulta estado, no procesa medios.

## 7. Problemas Comunes

* `job_id` inválido o inexistente.
* Consultar estado de trabajos eliminados tras completarse.

## 8. Buenas Prácticas

* Usar este endpoint para monitorizar tareas largas.
* Implementar manejo de errores en cliente.
* Evitar peticiones masivas: aplicar *rate limiting* o colas en el cliente.
