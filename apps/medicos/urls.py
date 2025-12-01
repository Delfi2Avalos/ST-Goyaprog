from django.urls import path
from . import views

urlpatterns = [
    path("turnos/<int:medicoId>/", views.ver_turnos),
    path("turnos/<int:turnoId>/", views.actualizar_estado_turno),
    path("ocupados/<int:medicoId>/<str:fecha>/", views.horas_ocupadas),

    path("horarios/<int:medicoId>/", views.obtener_horarios),
    path("actualizar-horarios/<int:medicoId>/", views.actualizar_horarios),

    path("cambiar-contrasena/<int:medicoId>/", views.cambiar_password),

    path("buscar-paciente/", views.buscar_paciente),

    path("formulario/", views.crear_formulario),
    path("formulario/<int:id>/", views.editar_formulario),
    path("formularios/<int:id>/", views.listar_formularios),

    path("formularios-nombre/<str:nombre>/", views.buscar_formularios_por_nombre),
]
