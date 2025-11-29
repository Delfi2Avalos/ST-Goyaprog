from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from .models import Usuario
from .serializers import (
    RegistroPacienteSerializer,
    LoginSerializer,
    UsuarioSerializer
)

from apps.firebase_integration.services import (
    firebase_set,
    firebase_update
)


# ==========================================================
# REGISTRO DE PACIENTE  (equivalente a tu Node.js)
# POST /api/usuarios/registro/
# ==========================================================

class RegistroPacienteView(APIView):
    def post(self, request):
        serializer = RegistroPacienteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usuario = serializer.save()  # crea el usuario

        # === Registro espejo en Firebase RTDB ===
        firebase_set(f"usuarios/pacientes/{usuario.id}", {
            "id_mysql": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "obra_social": usuario.obra_social,
            "detalles_extras": usuario.detalles_extras,
            "registrado_en": usuario.registrado_en.isoformat(),
        })

        return Response({
            "mensaje": "Usuario registrado correctamente.",
            "usuario": UsuarioSerializer(usuario).data
        }, status=status.HTTP_201_CREATED)


# ==========================================================
# LOGIN  (equivalente a tu Node.js)
# POST /api/usuarios/login/
# ==========================================================

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"].strip().lower()
        contrasena = serializer.validated_data["contrasena"]

        usuario = authenticate(request, email=email, password=contrasena)

        if usuario is None:
            return Response(
                {"mensaje": "Correo o contraseña incorrectos."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # GENERAR JWT (igual que Node)
        refresh = RefreshToken.for_user(usuario)

        # Actualizar última conexión
        usuario.ultima_conexion = timezone.now()
        usuario.save()

        # === Firebase update si es paciente ===
        if usuario.tipo == "paciente":
            firebase_update(f"usuarios/pacientes/{usuario.id}", {
                "ultima_conexion": usuario.ultima_conexion.isoformat()
            })

        return Response({
            "mensaje": "Login exitoso.",
            "token": str(refresh.access_token),
            "usuario": UsuarioSerializer(usuario).data
        }, status=status.HTTP_200_OK)
