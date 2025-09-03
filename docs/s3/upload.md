# S3 Upload API

El endpoint `/v1/s3/upload` permite transferir un archivo desde una URL remota directamente a un almacenamiento S3-compatible, sin usar disco local.

## Endpoint

```
POST /v1/s3/upload
```

## Autenticación

Requiere clave API en el header:

```
X-API-Key: YOUR_API_KEY
```

## Request

### Body (JSON)

| Parámetro | Tipo    | Req. | Descripción                                               |
| --------- | ------- | ---- | --------------------------------------------------------- |
| file\_url | string  | Sí   | URL del archivo a subir                                   |
| filename  | string  | No   | Nombre personalizado. Si no se indica, se usa el original |
| public    | boolean | No   | Hacer el archivo público (default: `false`)               |

Ejemplo:

```json
{
  "file_url": "https://example.com/path/to/file.mp4",
  "filename": "custom-name.mp4",
  "public": true
}
```

## Response

### Éxito (200 OK)

```json
{
  "url": "https://bucket-name.s3.region.amazonaws.com/custom-name.mp4",
  "filename": "custom-name.mp4",
  "bucket": "bucket-name",
  "public": true
}
```

| Campo    | Tipo    | Descripción                                                                    |
| -------- | ------- | ------------------------------------------------------------------------------ |
| url      | string  | URL de acceso al archivo (directa si es público, pre-firmada 1h si es privado) |
| filename | string  | Nombre final del archivo                                                       |
| bucket   | string  | Bucket de destino                                                              |
| public   | boolean | Indica si es accesible públicamente                                            |

### Error

```json
{
  "code": 400,
  "message": "Invalid request payload"
}
```

## Detalles Técnicos

* Se usa **Multipart Upload** de S3.
* El archivo se transmite en *chunks* desde la URL origen → S3.
* No se guarda en disco local.
* Soporta archivos grandes y subidas reanudables.

Pasos internos:

1. Se abre stream desde `file_url`.
2. Se suben partes a S3.
3. Se completa la subida multipart.
