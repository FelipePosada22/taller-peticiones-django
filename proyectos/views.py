# LIBRERIAS
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Proyecto


def leer_json(request):
    """Convierte el cuerpo de la petición (request.body) en un diccionario."""
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return None


# VISTA
@method_decorator(csrf_exempt, name="dispatch")
class ProyectoView(View):

    # GET -> READ: lista todos los proyectos o uno solo si llega el pk
    def get(self, request, pk=None):
        if pk is not None:
            proyecto = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse(proyecto.to_dict())
        proyectos = [p.to_dict() for p in Proyecto.objects.all()]
        return JsonResponse({"proyectos": proyectos})

    # POST -> CREATE: crea un proyecto nuevo
    def post(self, request):
        datos = leer_json(request)
        if datos is None or not datos.get("nombre"):
            return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)
        proyecto = Proyecto.objects.create(
            nombre=datos["nombre"],
            descripcion=datos.get("descripcion", ""),
        )
        return JsonResponse(proyecto.to_dict(), status=201)

    # PUT -> UPDATE: actualiza el proyecto indicado por pk
    def put(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        datos = leer_json(request)
        if datos is None:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        proyecto.nombre = datos.get("nombre", proyecto.nombre)
        proyecto.descripcion = datos.get("descripcion", proyecto.descripcion)
        proyecto.save()
        return JsonResponse(proyecto.to_dict())

    # DELETE -> DELETE: elimina el proyecto indicado por pk
    def delete(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return JsonResponse({"mensaje": f"Proyecto {pk} eliminado"})
