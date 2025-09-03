# Endpoint: Captura de Pantalla con Playwright

## ⚠️ Aviso

* Este endpoint **no está diseñado para saltar CAPTCHAs, Cloudflare** u otras protecciones anti-bots.
* **No se aceptan solicitudes** para añadir estas funciones.
* No funcionará en sitios con esas defensas y podría causar bloqueo de IP.
* Admite HTML, JavaScript y CSS personalizados como alternativa a usar una URL.
* Úsalo solo en sitios propios o con permiso explícito.

---

## 1. Descripción general

El endpoint `/v1/image/screenshot/webpage` permite capturar pantallas de páginas web con **Playwright**.
Soporta opciones avanzadas como tamaño de viewport, emulación de dispositivos, cookies, cabeceras, selectores y más.
Las capturas se suben a almacenamiento en la nube y se devuelve la URL.

---

## 2. Endpoint

* **Ruta:** `/v1/image/screenshot/webpage`
* **Método:** `POST`

---

## 3. Petición

### Cabeceras

* `x-api-key` (obligatorio): clave de la API.
* `Content-Type`: `application/json`

### Parámetros en el cuerpo

* `url` (string, obligatorio si no se usa `html`): URL de la página.
* `html` (string, opcional): HTML a renderizar (no combinar con `url`).
* `viewport_width`, `viewport_height` (int, opcional): tamaño en píxeles.
* `full_page` (bool, opcional, por defecto `false`): página completa.
* `format` (string, opcional): `png` o `jpeg` (por defecto `png`).
* `delay` (int, opcional): retraso en ms antes de capturar.
* `device_scale_factor` (número, opcional): escala de dispositivo (ej. 2).
* `user_agent` (string, opcional).
* `cookies` (array, opcional): lista de cookies `{name, value, domain}`.
* `headers` (objeto, opcional): cabeceras HTTP extra.
* `quality` (int, opcional, 0-100, solo para jpeg).
* `clip` (objeto, opcional): región `{x,y,width,height}`.
* `timeout` (int, opcional, mínimo 100).
* `wait_until` (string, opcional): `load`, `domcontentloaded`, `networkidle`.
* `wait_for_selector` (string, opcional).
* `emulate` (objeto, opcional): ej. `{ "color_scheme": "dark" }`.
* `omit_background` (bool, opcional, por defecto `false`).
* `selector` (string, opcional): selector CSS a capturar.
* `webhook_url` (string, opcional): para resultados asíncronos.
* `id` (string, opcional): identificador.
* `js` (string, opcional): código JS a inyectar antes de capturar.
* `css` (string, opcional): CSS a inyectar antes de capturar.

#### Ejemplo de petición

```json
{
  "url": "https://example.com",
  "viewport_width": 1280,
  "viewport_height": 720,
  "js": "document.body.style.background = 'red';",
  "css": "body { font-size: 30px; }",
  "full_page": true,
  "format": "png",
  "delay": 500,
  "device_scale_factor": 2,
  "user_agent": "CustomAgent/1.0",
  "cookies": [
    {"name": "test_cookie", "value": "test_value", "domain": "example.com", "path": "/"}
  ],
  "headers": {"Accept-Language": "es-ES,es;q=0.9"},
  "quality": 90,
  "clip": {"x": 0, "y": 0, "width": 800, "height": 600},
  "timeout": 10000,
  "wait_until": "networkidle",
  "wait_for_selector": "#main-content",
  "selector": "#main-content",
  "emulate": {"color_scheme": "dark"},
  "omit_background": true,
  "webhook_url": "https://miwebhook.com/callback",
  "id": "captura-001"
}
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "endpoint": "/v1/image/screenshot/webpage",
  "code": 200,
  "id": "captura-001",
  "job_id": "uuid-job",
  "response": "https://cloud.example.com/screenshot.png",
  "message": "success",
  "pid": 12345,
  "queue_id": 98765,
  "run_time": 2.345,
  "queue_time": 0.012,
  "total_time": 2.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Ejemplo de error

```json
{
  "endpoint": "/v1/image/screenshot/webpage",
  "code": 500,
  "id": "captura-001",
  "job_id": "uuid-job",
  "response": null,
  "message": "Detalles del error",
  "pid": 12345,
  "queue_id": 98765,
  "run_time": 0.123,
  "queue_time": 0.056,
  "total_time": 0.179,
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

---

## 5. Manejo de errores

* Parámetros inválidos/faltantes → 400
* API key inválida/faltante → 401
* Cola llena → 429
* Error en el proceso → 500

---

## 6. Notas de uso

* Con `webhook_url` el resultado se envía asíncronamente.
* Siempre se devuelve la URL en almacenamiento en la nube.
* Usa `selector` para capturar un elemento específico.
* Usa `clip` para capturar una región.
* Validación estricta del payload.

---

## 7. Problemas comunes

* URL inválida o inaccesible.
* Selector no encontrado.
* Cookies con dominio incorrecto.
* Timeout en páginas lentas.
* API key inválida.

---

## 8. Buenas prácticas

* Validar parámetros antes de enviar.
* Usar `id` únicos para rastreo.
* Manejar gracefully los errores 429.
* Usar siempre HTTPS.
* Probar selectores localmente antes de automatizar.