from django.urls import path
from . import views_admin

urlpatterns = [
    path("medicos-por-especialidad/<int:especialidad_id>/", views_admin.listar_medicos_por_especialidad),
    path("pacientes-atendidos/<int:medico_id>/", views_admin.contar_pacientes_atendidos),
    path("formularios/", views_admin.obtener_formularios),
    path("turnos/", views_admin.listar_turnos),
    path("actualizar-turno/", views_admin.actualizar_estado_turno),
    path("cancelar-turno/<int:turno_id>/", views_admin.cancelar_turno),
]
