# Detección de Silencios

El endpoint `/v1/media/silence` detecta intervalos de silencio en un archivo multimedia (audio o video). Permite configurar umbral de ruido, rango de tiempo y duración mínima de los silencios.

## Endpoint

```
POST /v1/media/silence
```

## Request

### Headers

* `x-api-key` (obligatorio): clave API.

### Body

```json
{
  "media_url": "https://example.com/audio.mp3",
  "start": "00:00:10.0",
  "end": "00:01:00.0",
  "noise": "-25dB",
  "duration": 0.5,
  "mono": false,
  "webhook_url": "https://example.com/webhook",
  "id": "unique-request-id"
}
```

| Parámetro    | Tipo    | Req. | Descripción                             |
| ------------ | ------- | ---- | --------------------------------------- |
| media\_url   | string  | Sí   | URL del archivo a analizar              |
| start        | string  | No   | Tiempo inicio `HH:MM:SS.ms`             |
| end          | string  | No   | Tiempo fin `HH:MM:SS.ms`                |
| noise        | string  | No   | Umbral de ruido en dB (default `-30dB`) |
| duration     | number  | Sí   | Duración mínima en seg. del silencio    |
| mono         | boolean | No   | Procesar en mono (default `true`)       |
| webhook\_url | string  | No   | URL para notificación asíncrona         |
| id           | string  | No   | Identificador de la petición            |

## Response

### Éxito (200 OK)

```json
{
  "endpoint": "/v1/media/silence",
  "code": 200,
  "id": "unique-request-id",
  "job_id": "a1b2c3d4",
  "response": [
    {"start": 10.5, "end": 15.2},
    {"start": 20.0, "end": 25.7}
  ],
  "message": "success",
  "run_time": 1.234,
  "total_time": 1.357
}
```

### Error (400 Bad Request)

```json
{
  "code": 400,
  "message": "Invalid request payload"
}
```

### Error (401 Unauthorized)

```json
{
  "code": 401,
  "message": "Unauthorized"
}
```

### Error (500 Internal Server Error)

```json
{
  "code": 500,
  "message": "An error occurred during the silence detection process"
}
```

## Notas

* `start` y `end` delimitan el rango a analizar.
* `noise` ajusta sensibilidad: valores bajos (ej. -40dB) detectan más silencios.
* `duration` evita falsos positivos en pausas muy cortas.
* Con `mono: true`, procesa solo un canal.

## Problemas comunes

* URL inválida o inaccesible.
* Tiempos fuera de rango.
* `duration` demasiado bajo → exceso de silencios detectados.

## Buenas prácticas

* Validar `media_url`.
* Usar `start` y `end` para limitar análisis.
* Ajustar `noise` y `duration` según el caso de uso.
* Configurar `webhook_url` para trabajos largos.
