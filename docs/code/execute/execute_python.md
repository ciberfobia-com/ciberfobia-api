# Endpoint: Ejecutar Código Python

## 1. Descripción general

El endpoint `/v1/code/execute/python` permite ejecutar código Python en el servidor.  
Forma parte de la API v1 definida en `app.py`. Proporciona un entorno seguro y controlado con validación de entrada, captura de salida y control de tiempos de ejecución.

---

## 2. Endpoint

- **Ruta:** `/v1/code/execute/python`  
- **Método:** `POST`

---

## 3. Petición

### Cabeceras

- `x-api-key` (obligatorio): clave de autenticación de la API.

### Parámetros en el cuerpo

El cuerpo debe ser un objeto JSON con:

- `code` (string, obligatorio): código Python a ejecutar.  
- `timeout` (integer, opcional): tiempo máximo de ejecución en segundos (1–300). Por defecto 30.  
- `webhook_url` (string, opcional): URL para recibir el resultado mediante webhook.  
- `id` (string, opcional): identificador único de la petición.  

**Esquema JSON:**

```json
{
  "type": "object",
  "properties": {
    "code": {"type": "string"},
    "timeout": {"type": "integer", "minimum": 1, "maximum": 300},
    "webhook_url": {"type": "string", "format": "uri"},
    "id": {"type": "string"}
  },
  "required": ["code"],
  "additionalProperties": false
}
````

### Ejemplo de petición

```json
{
  "code": "print('Hola Mundo')",
  "timeout": 10,
  "webhook_url": "https://example.com/webhook",
  "id": "peticion-unica-123"
}
```

**Ejemplo con cURL:**

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"code": "print(\"Hola Mundo\")", "timeout": 10, "webhook_url": "https://example.com/webhook", "id": "peticion-unica-123"}' \
     http://tu-api/v1/code/execute/python
```

---

## 4. Respuesta

### Ejemplo de éxito

```json
{
  "endpoint": "/v1/code/execute/python",
  "code": 200,
  "id": "peticion-unica-123",
  "job_id": "id-de-trabajo",
  "response": {
    "result": null,
    "stdout": "Hola Mundo\n",
    "stderr": "",
    "exit_code": 0
  },
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

### Ejemplos de error

**Parámetros inválidos (400):**

```json
{
  "error": "Missing or invalid parameters",
  "stdout": "",
  "exit_code": 400
}
```

**Error en ejecución (400):**

```json
{
  "error": "Mensaje de error",
  "stdout": "Salida parcial",
  "exit_code": 400
}
```

**Timeout (408):**

```json
{
  "error": "Execution timed out after 10 seconds"
}
```

**Error interno (500):**

```json
{
  "error": "An internal server error occurred",
  "stdout": "",
  "stderr": "",
  "exit_code": 500
}
```

---

## 5. Manejo de errores

* Parámetros inválidos → 400
* Errores en ejecución (sintaxis, excepciones) → 400
* Tiempo de ejecución superado → 408
* Errores internos → 500
* Sobrecarga de cola → 429

---

## 6. Notas de uso

* El código corre en un entorno aislado con recursos limitados.
* Tiempo máximo de ejecución: 300 segundos.
* La respuesta incluye stdout, stderr y código de salida.
* Con `webhook_url`, el resultado también se envía al webhook.

---

## 7. Problemas comunes

* Acceder a recursos restringidos genera error.
* Código pesado o bucles infinitos provocan timeout.
* `webhook_url` inválido evita recibir resultados externos.

---

## 8. Buenas prácticas

* Validar y sanear siempre las entradas de usuario.
* Usar `timeout` adecuado según la lógica del código.
* Revisar logs para detectar errores.
* Implementar límites y colas para evitar abusos.
* Considerar sandboxing adicional o filtrado de módulos.

```