# Taller – Peticiones en Django

**Curso:** Desarrollo de aplicaciones Web I – 4E
**Docente:** Jose Javier Torres Vanstrahlen

Endpoints REST construidos con **Django nativo** (sin Django REST Framework ni otras librerías externas), usando una vista basada en clase (`View`) con los métodos `get()`, `post()`, `put()` y `delete()`.

---

## 1. Cómo ejecutar el proyecto

```bash
python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 2. Estructura y archivos modificados

```
config/
  settings.py      -> se registra la app 'proyectos' en INSTALLED_APPS
  urls.py          -> se incluye proyectos.urls bajo el prefijo /api/
proyectos/
  models.py        -> modelo Proyecto (nombre, descripcion, creado)
  views.py         -> ProyectoView con get(), post(), put(), delete()
  urls.py          -> rutas del endpoint (archivo creado)
```

## 3. Verbos HTTP y su relación con CRUD

| Verbo HTTP | Operación CRUD | Método de la vista | Ruta | Respuesta exitosa |
|---|---|---|---|---|
| **GET** | **R**ead (leer) | `get(self, request, pk=None)` | `GET /api/proyectos/` · `GET /api/proyectos/<pk>/` | 200 OK |
| **POST** | **C**reate (crear) | `post(self, request)` | `POST /api/proyectos/` | 201 Created |
| **PUT** | **U**pdate (actualizar) | `put(self, request, pk)` | `PUT /api/proyectos/<pk>/` | 200 OK |
| **DELETE** | **D**elete (eliminar) | `delete(self, request, pk)` | `DELETE /api/proyectos/<pk>/` | 200 OK |

### Casos de uso de cada verbo

- **GET – Consultar.** Obtiene información sin modificar nada en el servidor (es *seguro* e *idempotente*). Uso típico: listar todos los registros o ver el detalle de uno por su id. Los parámetros viajan en la URL, nunca en el cuerpo.
- **POST – Crear.** Envía datos en el cuerpo de la petición para crear un recurso nuevo. **No** es idempotente: enviar la misma petición dos veces crea dos registros. Uso típico: formularios de registro o alta de un producto o proyecto.
- **PUT – Actualizar.** Reemplaza o modifica un recurso existente identificado por su `pk`. Es idempotente: repetir la misma petición deja el recurso en el mismo estado. Uso típico: editar los datos de un proyecto.
- **DELETE – Eliminar.** Borra el recurso identificado por su `pk`. Es idempotente: tras la primera eliminación, el recurso ya no existe (las siguientes peticiones devuelven 404). Uso típico: eliminar un registro.

Si llega un verbo que la vista no define (por ejemplo `PATCH`), Django responde automáticamente **405 Method Not Allowed**.

> **Nota sobre PUT y DELETE en Django:** Django solo llena `request.POST` en peticiones POST con datos de formulario. Para PUT y DELETE (y para JSON en general) el cuerpo se lee manualmente desde `request.body` y se convierte con `json.loads()`.

## 4. Ejemplos de uso (curl)

```bash
# CREATE
curl -X POST http://127.0.0.1:8000/api/proyectos/ \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Taller Django", "descripcion": "CRUD nativo"}'

# READ (lista y detalle)
curl http://127.0.0.1:8000/api/proyectos/
curl http://127.0.0.1:8000/api/proyectos/1/

# UPDATE
curl -X PUT http://127.0.0.1:8000/api/proyectos/1/ \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Taller Django (editado)"}'

# DELETE
curl -X DELETE http://127.0.0.1:8000/api/proyectos/1/
```

## 5. Módulos, funciones y decoradores de Django usados

| Elemento | Tipo | Módulo | Descripción |
|---|---|---|---|
| `View` | Clase | `django.views` | Vista base basada en clase. Su método `dispatch()` revisa el verbo HTTP de la petición y la envía al método con el mismo nombre (`get`, `post`, `put`, `delete`). Si no existe, responde 405. |
| `View.as_view()` | Método de clase | `django.views` | Convierte la clase en una función invocable que se puede registrar en `urls.py`. |
| `JsonResponse` | Clase | `django.http` | Subclase de `HttpResponse` que serializa un diccionario a JSON y añade la cabecera `Content-Type: application/json`. Permite fijar el código de estado con `status=`. |
| `HttpRequest` (`request`) | Objeto | `django.http` | Representa la petición entrante. Se usan `request.method` (verbo) y `request.body` (cuerpo en bytes). |
| `get_object_or_404()` | Función (atajo) | `django.shortcuts` | Busca un objeto en el modelo; si no existe lanza `Http404` y Django responde con 404. |
| `csrf_exempt` | Decorador | `django.views.decorators.csrf` | Desactiva la verificación del token CSRF para la vista. Es necesario para recibir POST/PUT/DELETE desde clientes que no son formularios de Django (curl, Postman, frontends). |
| `method_decorator` | Decorador | `django.utils.decorators` | Adapta un decorador de funciones (como `csrf_exempt`) para aplicarlo a los métodos de una clase. Con `name="dispatch"` afecta a todos los verbos de la vista. |
| `path()` | Función | `django.urls` | Define una ruta URL y la asocia con una vista. Admite convertidores como `<int:pk>` para capturar parámetros. |
| `include()` | Función | `django.urls` | Incluye el `urls.py` de una app dentro del `urls.py` principal del proyecto. |
| `models.Model` | Clase | `django.db.models` | Clase base de los modelos (ORM). Proporciona `objects.all()`, `objects.create()`, `save()` y `delete()`, usados en cada operación CRUD. |
| `json` | Módulo | Biblioteca estándar de Python | `json.loads()` convierte el cuerpo de la petición (texto JSON) en un diccionario de Python. |

> **Decorador alternativo (para vistas basadas en función):** `django.views.decorators.http.require_http_methods(["GET", "POST"])` restringe los verbos permitidos. En vistas basadas en clase no hace falta, porque `View` ya lo controla con `http_method_names`.

## 6. Fuentes consultadas

1. Django Documentation – *Class-based views*: https://docs.djangoproject.com/en/stable/topics/class-based-views/
2. Django Documentation – *Base views (`View`, `dispatch`, `as_view`)*: https://docs.djangoproject.com/en/stable/ref/class-based-views/base/
3. Django Documentation – *Request and response objects (`HttpRequest`, `JsonResponse`)*: https://docs.djangoproject.com/en/stable/ref/request-response/
4. Django Documentation – *Django shortcut functions (`get_object_or_404`)*: https://docs.djangoproject.com/en/stable/topics/http/shortcuts/
5. Django Documentation – *Cross Site Request Forgery protection (`csrf_exempt`)*: https://docs.djangoproject.com/en/stable/ref/csrf/
6. Django Documentation – *Decorating class-based views (`method_decorator`)*: https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/#decorating-class-based-views
7. Django Documentation – *View decorators (`require_http_methods`)*: https://docs.djangoproject.com/en/stable/topics/http/decorators/
8. Django Documentation – *URL dispatcher (`path`, `include`)*: https://docs.djangoproject.com/en/stable/topics/http/urls/
9. MDN Web Docs – *HTTP request methods*: https://developer.mozilla.org/es/docs/Web/HTTP/Methods
10. RFC 9110 – *HTTP Semantics, sección 9 (Methods)*: https://www.rfc-editor.org/rfc/rfc9110#section-9
