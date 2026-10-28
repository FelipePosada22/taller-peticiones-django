from django.urls import path

from .views import ProyectoView

urlpatterns = [
    # GET (listar) y POST (crear)
    path("proyectos/", ProyectoView.as_view(), name="proyectos"),
    # GET (detalle), PUT (actualizar) y DELETE (eliminar)
    path("proyectos/<int:pk>/", ProyectoView.as_view(), name="proyecto_detalle"),
]
