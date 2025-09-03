# Authenticate Endpoint

## 1. Descripción

El endpoint `/v1/toolkit/authenticate` forma parte del *blueprint* `v1_toolkit_auth`. Su función es autenticar las peticiones verificando la clave API (`X-API-Key`). Actúa como puerta de entrada para asegurar que solo clientes autorizados accedan a los recursos.

## 2. Endpoint

* **URL Path:** `/v1/toolkit/authenticate`
* **HTTP Method:** `GET`

## 3. Request

### Headers

* `X-API-Key` (**requerido**): clave API para autenticación.

### Body

No requiere parámetros en el body.

### Ejemplo

```bash
curl -X GET -H "X-API-Key: YOUR_API_KEY" http://localhost:8080/v1/toolkit/authenticate
```

## 4. Response

### Éxito (200 OK)

```json
{
  "code": 200,
  "endpoint": "/authenticate",
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "success",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "response": "Authorized",
  "run_time": 0.001,
  "total_time": 0.001,
  "queue_time": 0,
  "build_number": "1.0.0"
}
```

### Error (401 Unauthorized)

```json
{
  "code": 401,
  "endpoint": "/authenticate",
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "Unauthorized",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "response": null,
  "run_time": 0.001,
  "total_time": 0.001,
  "queue_time": 0,
  "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

* API key inválida o ausente → **401 Unauthorized**.

## 6. Notas de Uso

* Diseñado como puerta de seguridad para el resto de endpoints.
* La API key debe mantenerse privada.

## 7. Problemas Comunes

* Olvidar el header `X-API-Key`.
* Usar clave inválida o expirada.

## 8. Buenas Prácticas

* Rotar las claves periódicamente.
* No exponer claves en repositorios o código público.
* Añadir medidas extra como *rate limiting* o listas blancas de IPs.