from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "nombre",
            "apellido",
            "email",
            "tipo",
            "obra_social",
            "detalles_extras",
            "registrado_en",
            "ultima_conexion",
        ]
        read_only_fields = ["id", "registrado_en", "ultima_conexion"]


class RegistroPacienteSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "nombre",
            "apellido",
            "email",
            "contrasena",
            "obra_social",
            "detalles_extras",
        ]

    def create(self, validated_data):
        contrasena = validated_data.pop("contrasena")
        usuario = Usuario.objects.create_user(
            email=validated_data["email"],
            contrasena=contrasena,
            tipo="paciente",  # Fijo igual que Node.js
            **validated_data
        )
        return usuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    contrasena = serializers.CharField(write_only=True)
