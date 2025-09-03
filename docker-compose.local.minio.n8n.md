# Desarrollo Local con MinIO y n8n

Este entorno proporciona un setup completo para desarrollo local de **Ciberfobia API**, con almacenamiento S3-compatible (MinIO) y automatización de flujos con **n8n**.

## Incluye

- **Ciberfobia API**: compilada desde el código fuente.
- **MinIO**: almacenamiento S3 con consola web.
- **n8n**: plataforma de automatización de flujos.
- **Red Docker dedicada**: comunicación interna entre servicios.
- **Persistencia**: datos conservados entre reinicios.

---

## Requisitos

- Docker + Docker Compose
- Git
- 2GB RAM libre
- 5GB espacio libre en disco

---

## Inicio Rápido

### 1. Configurar entorno

```bash
cp .env.local.minio.n8n.example .env.local.minio.n8n
````

Edita `.env.local.minio.n8n` según tus necesidades.

### 2. Levantar servicios

```bash
docker compose -f docker-compose.local.minio.n8n.yml up -d
```

### 3. Accesos

* **Ciberfobia API**: [http://localhost:8080](http://localhost:8080)
* **n8n**: [http://localhost:5678](http://localhost:5678)
* **MinIO Console**: [http://localhost:9001](http://localhost:9001)

  * Usuario: `minioadmin`
  * Pass: `minioadmin123`

### 4. Verificar

```bash
curl -H "x-api-key: local-dev-key-123" http://localhost:8080/v1/toolkit/test
```

---

## Configuración

### App

```env
APP_NAME=CiberfobiaAPI
APP_DEBUG=true
APP_DOMAIN=localhost:8080
APP_URL=http://localhost:8080
API_KEY=local-dev-key-123
```

### MinIO

```env
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123
S3_REGION=us-east-1
S3_BUCKET_NAME=ciberfobia-api-local
```

### n8n

```env
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/
```

---

## Servicios

* **Ciberfobia API**: puerto 8080, conecta a MinIO.
* **MinIO**: API en [http://localhost:9000](http://localhost:9000), consola en [http://localhost:9001](http://localhost:9001).
* **n8n**: interfaz en [http://localhost:5678](http://localhost:5678).

---

## Flujo de Desarrollo

### Recompilar API

```bash
docker compose -f docker-compose.local.minio.n8n.yml build ncat
docker compose -f docker-compose.local.minio.n8n.yml up -d
```

### Logs

```bash
docker compose -f docker-compose.local.minio.n8n.yml logs -f
docker compose -f docker-compose.local.minio.n8n.yml logs -f ncat
```

### MinIO Console

[http://localhost:9001](http://localhost:9001)
Bucket: `ciberfobia-api-local`

Reset:

```bash
docker compose -f docker-compose.local.minio.n8n.yml down
docker volume rm ciberfobia_minio_data
docker compose -f docker-compose.local.minio.n8n.yml up -d
```

---

## Comunicación entre servicios

* n8n → API: `http://ncat:8080`
* n8n → MinIO: `http://minio:9000`
* API → MinIO: `http://minio:9000`

### Ejemplo n8n

Request node:

```json
{
  "method": "GET",
  "url": "http://ncat:8080/v1/toolkit/test",
  "headers": {
    "x-api-key": "local-dev-key-123"
  }
}
```

---

## Persistencia

* Volúmenes: `storage`, `logs`, `minio_data`, `n8n_data`
* Directorio compartido: `./local-files`

---

## Problemas comunes

### Servicios no arrancan

```bash
docker compose -f docker-compose.local.minio.n8n.yml ps
docker compose -f docker-compose.local.minio.n8n.yml logs
```

### Puertos en uso

Editar `docker-compose.local.minio.n8n.yml`:

```yaml
ports:
  - "8081:8080"
```

### API key inválida

Usar la definida en `.env.local.minio.n8n`.

---

## Parar entorno

```bash
docker compose -f docker-compose.local.minio.n8n.yml down
docker compose -f docker-compose.local.minio.n8n.yml down -v  # borra datos
```

---

## Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Ciberfobia API │    │       n8n       │    │      MinIO      │
│   localhost:8080│◄──►│   localhost:5678│◄──►│  localhost:9000 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 │
                      ┌─────────────────┐
                      │ MinIO Console   │
                      │ localhost:9001  │
                      └─────────────────┘
```
