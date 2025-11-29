from rest_framework import serializers
from .models import Usuario

class RegistroPacienteSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "nombre", "apellido", "email",
            "contrasena", "tipo", "obra_social", "detalles_extras"
        ]

    def validate_tipo(self, value):
        if value != "paciente":
            raise serializers.ValidationError("Solo se puede registrar pacientes desde esta vía.")
        return value

    def create(self, validated_data):
        contrasena = validated_data.pop("contrasena")
        usuario = Usuario.objects.create_user(
            contrasena=contrasena,
            **validated_data
        )
        return usuario
