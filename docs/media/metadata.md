# Metadatos de Medios

Este endpoint extrae metadatos detallados de archivos multimedia (video, audio, imagen), incluyendo formato, duración, códecs, resolución y bitrates.

## Endpoint

`POST /v1/media/metadata`

## Autenticación

Este endpoint requiere autenticación por API. Ver [Autenticación](../toolkit/authenticate.md) para más detalles.

## Request

```json
{
  "media_url": "https://example.com/media.mp4",
  "webhook_url": "https://example.com/webhook",  
  "id": "custom-id"  
}
```

| Parámetro    | Tipo   | Requerido | Descripción                                  |
| ------------ | ------ | --------- | -------------------------------------------- |
| media\_url   | string | Sí        | URL del archivo a analizar                   |
| webhook\_url | string | No        | URL para recibir el resultado al terminar    |
| id           | string | No        | Identificador personalizado para la petición |

## Response

**Éxito (200 OK)**

```json
{
  "code": 200,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "id": "custom-id",
  "response": {
    "filesize": 15679283,
    "filesize_mb": 14.95,
    "duration": 87.46,
    "duration_formatted": "00:01:27.46",
    "format": "mp4,mov,m4a,3gp,3g2,mj2",
    "overall_bitrate": 1438692,
    "overall_bitrate_mbps": 1.44,
    "has_video": true,
    "video_codec": "h264",
    "video_codec_long": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
    "width": 1920,
    "height": 1080,
    "resolution": "1920x1080",
    "fps": 30.0,
    "video_bitrate": 1300000,
    "video_bitrate_mbps": 1.3,
    "pixel_format": "yuv420p",
    "has_audio": true,
    "audio_codec": "aac",
    "audio_codec_long": "AAC (Advanced Audio Coding)",
    "audio_channels": 2,
    "audio_sample_rate": 48000,
    "audio_sample_rate_khz": 48.0,
    "audio_bitrate": 128000,
    "audio_bitrate_kbps": 128
  },
  "message": "success",
  "run_time": 0.542,
  "queue_time": 0,
  "total_time": 0.542,
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "123"
}
```

En archivos solo de audio, los campos de video no estarán presentes. En archivos de video sin audio, no se incluirán los campos de audio.

**En cola (202 Accepted)**

```json
{
  "code": 202,
  "id": "custom-id",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 0,
  "build_number": "123"
}
```

**Error (4xx/5xx)**

```json
{
  "code": 500,
  "id": "custom-id",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Error extracting metadata: [detalles del error]",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 0,
  "build_number": "123"
}
```

## Ejemplo

### Request

```bash
curl -X POST https://api.example.com/v1/media/metadata \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "media_url": "https://example.com/sample-video.mp4",
    "webhook_url": "https://your-server.com/webhook"
  }'
```

### Response

```json
{
  "code": 200,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": {
    "filesize": 15679283,
    "filesize_mb": 14.95,
    "duration": 87.46,
    "duration_formatted": "00:01:27.46",
    "format": "mp4",
    "overall_bitrate": 1438692,
    "overall_bitrate_mbps": 1.44,
    "has_video": true,
    "video_codec": "h264",
    "width": 1920,
    "height": 1080,
    "resolution": "1920x1080",
    "fps": 30.0,
    "video_bitrate": 1300000,
    "video_bitrate_mbps": 1.3,
    "has_audio": true,
    "audio_codec": "aac",
    "audio_channels": 2,
    "audio_sample_rate": 48000,
    "audio_bitrate": 128000,
    "audio_bitrate_kbps": 128
  },
  "message": "success",
  "run_time": 0.542,
  "total_time": 0.542
}
```
