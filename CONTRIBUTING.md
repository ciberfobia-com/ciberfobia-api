# Contribuyendo a Ciberfobia API

Gracias por tu interés en contribuir ❤️

Este proyecto existe para ayudar a que **creadores no técnicos construyan sistemas inteligentes** — así que cada contribución debe seguir estos principios:

✅ Simple
✅ Útil
✅ Bajo mantenimiento

El repositorio está enfocado en nuevas contribuciones y desarrollo de features. Todos los PR deben traer código completo, probado y listo para revisión. No aceptamos envíos que requieran limpieza, debug o trabajo extra de los mantenedores.

> Si te gusta el proyecto pero no sabes programar, también puedes apoyar:
>
> * ⭐ Dale una estrella al repo
> * 📣 Compártelo en redes
> * 🌲 Refiérelo a un amigo o comunidad
> * 💸 [Patrocina el proyecto](#)

Si necesitas ayuda o tienes dudas, revisa las [discusiones en GitHub](https://github.com/ciberfobia/ciberfobia-api/discussions) o únete a la [comunidad](https://ciberfobia.com/whatsapp).

---

## Tabla de Contenidos

* [Qué Aceptamos](#qué-aceptamos-)
* [Qué Rechazamos](#qué-rechazamos-)
* [Framework de Evaluación](#framework-de-evaluación)
* [Guías Técnicas](#guías-técnicas)
* [Tipos de Contribución](#tipos-de-contribución)
* [Convenciones de Ramas](#convenciones-de-ramas)
* [Notas Finales](#notas-finales-)

---

## Qué Aceptamos ✅

* Resuelve **retos comunes no-code**
* **Reduce costes** o reemplaza APIs/herramientas de pago
* Requiere mínima configuración (tiene defaults)
* Entendible por usuarios **no técnicos**
* Funciona out-of-the-box
* Integraciones únicas — **no requieren mantenimiento continuo**
* Usa **nombres de inputs/outputs estándar**
* Respeta la estructura del repo

---

## Qué Rechazamos ❌

* Features hechos para un solo caso o edge-case
* Inconsistencia en nombres de inputs/outputs
* Necesita polling, retries o callbacks
* Requiere babysitting o falla seguido
* Sin manejo de errores ni comentarios
* Código o dependencias sin usar
* Añade paquetes pesados que inflan la imagen de Docker
* Deja trabajo pendiente a los mantenedores

---

## Framework de Evaluación

| Categoría             | Pregunta                              | ✅ Aceptar si...                           | ❌ Rechazar si...                  |
| --------------------- | ------------------------------------- | ----------------------------------------- | --------------------------------- |
| **Misión**            | ¿Reduce coste o unifica herramientas? | Reemplaza APIs, reduce costes/complexidad | Añade ruido, casos muy concretos  |
| **Inputs Familiares** | ¿Usa inputs conocidos? (`file_url`)   | Usa nombres/tipos ya estándar             | Introduce términos nuevos         |
| **Claridad Input**    | ¿Un no-técnico sabe qué poner?        | Inputs como "Enter URL", "Choose format"  | Requiere explicación técnica      |
| **Outputs Útiles**    | ¿Sirve directo en Make/Zapier?        | Devuelve archivos limpios, texto, URLs    | Datos crudos o nested complejos   |
| **Fiabilidad**        | ¿Funciona sin babysitting?            | API estable, comportamiento consistente   | API inestable o propensa a fallos |
| **Mantenimiento**     | ¿Requiere cuidado?                    | One-and-done, no cambia seguido           | Cambios frecuentes del vendor     |
| **Valor vs Esfuerzo** | ¿Vale la pena?                        | Alto impacto, muy pedido                  | Nicho, bajo ROI                   |

---

## Guías Técnicas

### 🧠 Estilo de Código

* Nombres descriptivos (`convertImageToText`, no `imgTxt`)
* Comenta la lógica no obvia
* Maneja errores, no fallos silenciosos
* Formato consistente

### 🧼 Contribuciones Limpias

* No cambies archivos no relacionados
* No dejes dependencias o código sin usar
* No metas dependencias pesadas
* Usa `git status` antes de commitear

---

## Convenciones de Ramas

1. Haz fork del [repo principal](https://github.com/ciberfobia/ciberfobia-api)
2. Clona tu fork:

   ```bash
   git clone https://github.com/TU_USUARIO/ciberfobia-api.git
   cd ciberfobia-api
   ```
3. Añade upstream:

   ```bash
   git remote add upstream https://github.com/ciberfobia/ciberfobia-api.git
   ```
4. Crea branch desde `build`:

   ```bash
   git fetch upstream
   git checkout -b feature/nombre upstream/build
   ```
5. Nombra ramas así:

   * Bugfix: `fix/nombre-bug`
   * Feature: `feature/nueva-funcionalidad`
   * Docs: `docs/cambio-docs`

Ejemplo:

```bash
git checkout -b feature/pdf-to-text upstream/build
git checkout -b fix/webp-upload upstream/build
```

6. Push y PR a `build`:

```bash
git push origin feature/pdf-to-text
```

---

## Tipos de Contribución

| Tipo      | Ejemplo                                               |
| --------- | ----------------------------------------------------- |
| 🐞 Bug    | "Arregla crash al subir archivos WebP"                |
| ⚡ Feature | "Añade endpoint que reemplaza API de pago"            |
| 📚 Docs   | "Mejora docs de despliegue (Netlify, AWS, Vercel...)" |

---

## Notas Finales 🧘‍♂️

* Si no está listo, no lo subas
* Debe ser útil, obvio y bajo mantenimiento
* Meta: **hacer simple lo complejo para usuarios no-code**

🎉 ¡Esperamos tus contribuciones!
