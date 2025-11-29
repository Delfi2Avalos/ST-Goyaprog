from django.urls import path
from . import views_superadmin

urlpatterns = [
    path("medicos-por-especialidad/<int:especialidad_id>/", views_superadmin.listar_medicos_por_especialidad),
    path("pacientes-atendidos/<int:medico_id>/", views_superadmin.contar_pacientes_atendidos),
    path("registrar-medico/", views_superadmin.registrar_medico),
    path("formularios/", views_superadmin.obtener_formularios),
    path("crear-admin/", views_superadmin.crear_secretario),
]
