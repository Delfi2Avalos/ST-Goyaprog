from django.urls import path
from .views import RegistroPacienteView, LoginView

urlpatterns = [
    path("registro/", RegistroPacienteView.as_view()),
    path("login/", LoginView.as_view()),
]
