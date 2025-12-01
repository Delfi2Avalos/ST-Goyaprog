from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsMedico
from .services import MedicoService

@api_view(["GET"])
@permission_classes([IsMedico])
def ver_turnos(request, medicoId):
    turnos = MedicoService.ver_turnos(medicoId)
    return Response(turnos, status=200)

@api_view(["PUT"])
@permission_classes([IsMedico])
def actualizar_estado_turno(request, turnoId):
    estado = request.data.get("estado")
    ok, error = MedicoService.actualizar_estado_turno(turnoId, estado)
    if error:
        return Response({"mensaje": error}, status=400)
    return Response({"mensaje": "Estado actualizado correctamente"}, status=200)

@api_view(["GET"])
@permission_classes([IsMedico])
def obtener_horarios(request, medicoId):
    horarios = MedicoService.obtener_horarios(medicoId)
    return Response(horarios)

@api_view(["PUT"])
@permission_classes([IsMedico])
def actualizar_horarios(request, medicoId):
    horarios = request.data.get("horarios")
    MedicoService.actualizar_horarios(medicoId, horarios)
    return Response({"mensaje": "Horarios actualizados correctamente"})

@api_view(["GET"])
@permission_classes([IsMedico])
def horas_ocupadas(request, medicoId, fecha):
    horas = MedicoService.horas_ocupadas(medicoId, fecha)
    return Response(horas)

@api_view(["PUT"])
@permission_classes([IsMedico])
def cambiar_password(request, medicoId):
    nueva = request.data.get("nueva_contrasena")
    MedicoService.cambiar_password(medicoId, nueva)
    return Response({"mensaje": "Contraseña actualizada correctamente"})

@api_view(["GET"])
@permission_classes([IsMedico])
def buscar_paciente(request):
    nombre = request.query_params.get("nombre")
    apellido = request.query_params.get("apellido")
    paciente = MedicoService.buscar_paciente(nombre, apellido)
    if not paciente:
        return Response({"mensaje": "Paciente no encontrado"}, status=404)
    return Response(paciente)

@api_view(["POST"])
@permission_classes([IsMedico])
def crear_formulario(request):
    medico_id = request.data.get("medico_id")
    nombre_completo = request.data.get("nombre_completo")
    contenido = request.data.get("contenido")
    MedicoService.crear_formulario(medico_id, nombre_completo, contenido)
    return Response({"mensaje": "Formulario guardado exitosamente"}, status=201)

@api_view(["PUT"])
@permission_classes([IsMedico])
def editar_formulario(request, id):
    contenido = request.data.get("contenido")
    nombre_completo = request.data.get("nombre_completo")
    MedicoService.editar_formulario(id, contenido, nombre_completo)
    return Response({"mensaje": "Formulario actualizado correctamente"})

@api_view(["GET"])
@permission_classes([IsMedico])
def listar_formularios(request, id):
    formularios = MedicoService.listar_formularios(id)
    return Response(formularios)

@api_view(["GET"])
@permission_classes([IsMedico])
def buscar_formularios_por_nombre(request, nombre):
    data = MedicoService.buscar_formularios_por_nombre(nombre)
    if not data:
        return Response({"mensaje": "No se encontraron formularios"}, status=404)
    return Response(data)
