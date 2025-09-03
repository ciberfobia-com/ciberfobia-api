# Instalar Ciberfobia API con Docker

La instalación de Ciberfobia API con Docker ofrece las siguientes ventajas:

* Instalar Ciberfobia API en un entorno limpio.
* Simplificar el proceso de configuración.
* Evitar problemas de compatibilidad entre diferentes sistemas operativos con el entorno consistente de Docker.

> **Info**
> Si tu dominio/subdominio ya está apuntando al servidor, comienza en el paso 2.
> Si ya tienes instalado Docker y Docker-Compose, comienza en el paso 3.

---

## 1. Configuración de DNS

Apunta tu dominio/subdominio al servidor. Añade un registro A para redirigir el dominio/subdominio:

* **Type**: A
* **Name**: El dominio/subdominio deseado
* **IP Address**: `<IP_OF_YOUR_SERVER>`

---

## 2. Instalar Docker

Esto puede variar dependiendo de la distribución de Linux utilizada. A continuación, las instrucciones para Ubuntu:

### Configurar el repositorio APT de Docker

```bash
# Añadir la clave GPG oficial de Docker:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Añadir el repositorio a las fuentes de APT:
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### Instalar los paquetes de Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 3. Crear archivo Docker Compose

Crea un archivo `docker-compose.yml` y pega la siguiente configuración:

### Con soporte SSL

Habilita SSL/TLS para comunicaciones seguras y encriptadas. Ideal para quienes quieren un enfoque automático con SSL.

```yaml
services:
  traefik:
    image: "traefik"
    restart: unless-stopped
    command:
      - "--api=true"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.mytlschallenge.acme.tlschallenge=true"
      - "--certificatesresolvers.mytlschallenge.acme.email=${SSL_EMAIL}"
      - "--certificatesresolvers.mytlschallenge.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - traefik_data:/letsencrypt
      - /var/run/docker.sock:/var/run/docker.sock:ro
  ncat:
    image: ciberfobia/ciberfobia-api:latest
    env_file:
      - .env
    labels:
      - traefik.enable=true
      - traefik.http.routers.ncat.rule=Host(`${APP_DOMAIN}`)
      - traefik.http.routers.ncat.tls=true
      - traefik.http.routers.ncat.entrypoints=web,websecure
      - traefik.http.routers.ncat.tls.certresolver=mytlschallenge
    volumes:
      - storage:/var/www/html/storage/app
      - logs:/var/www/html/storage/logs
    restart: unless-stopped

volumes:
  traefik_data:
    driver: local
  storage:
    driver: local
  logs:
    driver: local
```

---

## 4. Crear archivo `.env`

Crea un archivo `.env` y configúralo de la siguiente manera:

```env
# El nombre de tu aplicación.
APP_NAME=CiberfobiaAPI

# Ajuste del modo de depuración. Ponlo en `false` para entornos de producción.
APP_DEBUG=false

# Dominio o subdominio de tu aplicación, sin 'http://' o 'https://'.
APP_DOMAIN=example.com

# La URL completa de la aplicación se configura automáticamente; no requiere modificación.
APP_URL=https://${APP_DOMAIN}

# Configuración SSL
SSL_EMAIL=user@example.com

# API_KEY
# Propósito: Usada para autenticación de la API.
# Requisito: Obligatorio.
API_KEY=your_api_key_here

# Variables de entorno de almacenamiento compatible con s3
#
#S3_ACCESS_KEY=your_access_key
#S3_SECRET_KEY=your_secret_key
#S3_ENDPOINT_URL=https://your-endpoint-url
#S3_REGION=your-region
#S3_BUCKET_NAME=your-bucket-name


# Variables de entorno de Google Cloud Storage
#
# GCP_SA_CREDENTIALS
# Propósito: Credenciales JSON de la cuenta de servicio de GCP.
# Requisito: Obligatorio si usas almacenamiento GCP.
#GCP_SA_CREDENTIALS=/path/to/your/gcp/service_account.json

# GCP_BUCKET_NAME
# Propósito: Nombre del bucket de almacenamiento en GCP.
# Requisito: Obligatorio si usas almacenamiento GCP.
#GCP_BUCKET_NAME=your_gcp_bucket_name

# STORAGE_PATH
# Propósito: Ruta base para operaciones de almacenamiento.
# Valor por defecto: GCP
# Requisito: Opcional.
#STORAGE_PATH=GCP
```

---

## 5. Iniciar Docker Compose

Inicia Ciberfobia API con el siguiente comando:

```bash
docker compose up -d
```

Para ver los logs en tiempo real:

```bash
docker compose logs -f
```

Para detener los contenedores:

```bash
docker compose stop
```

Para reiniciar y recargar variables del `.env`:

```bash
docker compose up -d --force-recreate ncat
```

---

## 6. Finalizado

Ciberfobia API ahora está accesible a través de la APP\_URL especificada. 
Por ejemplo: [https://example.com](https://example.com)
