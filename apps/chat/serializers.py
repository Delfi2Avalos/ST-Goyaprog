from rest_framework import serializers
from .models import Conversacion, MensajeChat

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = "__all__"


class ConversacionSerializer(serializers.ModelSerializer):
    ultimo_mensaje = serializers.SerializerMethodField()

    class Meta:
        model = Conversacion
        fields = ["id", "paciente", "admin", "estado", "fecha_inicio", "ultimo_mensaje"]

    def get_ultimo_mensaje(self, obj):
        last_msg = obj.mensajes.order_by("-fecha_envio").first()
        return last_msg.mensaje if last_msg else None
