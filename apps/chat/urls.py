from django.urls import path
from .views import (
    EnviarMensajeAPIView,
    ObtenerConversacionAPIView,
    ObtenerChatsUsuarioAPIView
)

urlpatterns = [
    path("enviar/", EnviarMensajeAPIView.as_view()),
    path("mensajes/<int:conversacion_id>/", ObtenerConversacionAPIView.as_view()),
    path("usuario/<int:usuario_id>/", ObtenerChatsUsuarioAPIView.as_view()),
]
