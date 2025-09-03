# Portal de Feedback de Medios

Este endpoint sirve una página web estática para recopilar feedback sobre medios.

---

## Endpoint

```
GET /v1/media/feedback
```

### Autenticación

No requiere autenticación, es de acceso público.

### Respuesta

Devuelve la página HTML con el formulario de feedback.

---

## Archivos estáticos

Archivos adicionales (CSS, JavaScript, imágenes) pueden accederse en:

```
GET /v1/media/feedback/<filename>
```

Reemplaza `<filename>` con la ruta del recurso estático relativo al directorio.

---

## Desarrollo

Los archivos de la web están en:

```
services/v1/media/feedback/static/
```

Contenido:

* `index.html` – Archivo principal HTML
* `css/styles.css` – Hoja de estilos
* `js/script.js` – Código JavaScript
* `images/` – Carpeta para recursos gráficos

Para modificar la página de feedback, edita directamente estos archivos.
