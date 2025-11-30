from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Conversacion, MensajeChat
from usuarios.models import Usuario
from .serializers import MensajeSerializer, ConversacionSerializer


class ObtenerConversacionAPIView(APIView):

    def get(self, request, conversacion_id):
        conversacion = Conversacion.objects.get(id=conversacion_id)
        mensajes = conversacion.mensajes.order_by("fecha_envio")

        serializer = MensajeSerializer(mensajes, many=True)
        return Response(serializer.data)


class ObtenerChatsUsuarioAPIView(APIView):

    def get(self, request, usuario_id):
        usuario = Usuario.objects.get(id=usuario_id)

        if usuario.tipo == "admin":
            conversaciones = Conversacion.objects.filter(
                Q(admin=usuario) | Q(admin__isnull=True)
            )
        else:
            conversaciones = Conversacion.objects.filter(paciente=usuario)

        serializer = ConversacionSerializer(conversaciones, many=True)
        return Response(serializer.data)
