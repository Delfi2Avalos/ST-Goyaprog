from django.urls import path
from .views import RegistroPacienteView, LoginView

urlpatterns = [
    path("registro/", RegistroPacienteView.as_view(), name="registro_paciente"),
    path("login/", LoginView.as_view(), name="login"),
]
