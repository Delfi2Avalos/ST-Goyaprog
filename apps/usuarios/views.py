from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone

from .serializers import RegistroPacienteSerializer
from .models import Usuario
from .services import enviar_correo_alta, sync_paciente_firebase

from apps.firebase_integration.services import initialize_firebase
rtdb = initialize_firebase()

# REGISTRO PACIENTE
class RegistroPacienteView(APIView):
    def post(self, request):
        serializer = RegistroPacienteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        usuario = serializer.save()

        enviar_correo_alta(usuario.nombre, usuario.email)

        # SUBE A FIREBASE
        sync_paciente_firebase(rtdb, usuario.id, {
            "id_mysql": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "obra_social": usuario.obra_social,
            "detalles_extras": usuario.detalles_extras,
            "registrado_en": usuario.registrado_en.isoformat()
        })

        return Response({
            "mensaje": "Usuario registrado correctamente.",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "tipo": usuario.tipo,
                "obra_social": usuario.obra_social,
            }
        }, status=201)


# LOGIN
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        contrasena = request.data.get("contrasena")

        user = authenticate(request, email=email, password=contrasena)

        if not user:
            return Response({"mensaje": "Correo o contraseña incorrectos."}, status=401)

        refresh = RefreshToken.for_user(user)

        # Actualizar conexión si es paciente
        if user.tipo == "paciente":
            user.ultima_conexion = timezone.now()
            user.save()

            if rtdb:
                rtdb.ref(f"usuarios/pacientes/{user.id}").update({
                    "ultima_conexion": user.ultima_conexion.isoformat()
                })

        return Response({
            "mensaje": "Login exitoso.",
            "token": str(refresh.access_token),
            "usuario": {
                "id": user.id,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "email": user.email,
                "tipo": user.tipo,
                "obra_social": user.obra_social,
            }
        })
