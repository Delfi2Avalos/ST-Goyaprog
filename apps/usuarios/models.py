from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


# =====================================
# MANAGER PERSONALIZADO
# =====================================

class UsuarioManager(BaseUserManager):
    def create_user(self, email, contrasena=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if contrasena:
            user.set_password(contrasena)
        else:
            raise ValueError("La contraseña es obligatoria")

        user.save(using=self._db)
        return user

    def create_superuser(self, email, contrasena=None, **extra_fields):
        extra_fields.setdefault("tipo", "superadmin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, contrasena, **extra_fields)


# =====================================
# MODELO USUARIO
# =====================================

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_CHOICES = [
        ("paciente", "Paciente"),
        ("medico", "Médico"),
        ("admin", "Admin"),
        ("superadmin", "SuperAdmin"),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="paciente")

    obra_social = models.CharField(max_length=100, null=True, blank=True)
    detalles_extras = models.TextField(null=True, blank=True)

    registrado_en = models.DateTimeField(default=timezone.now)
    ultima_conexion = models.DateTimeField(null=True, blank=True)

    # Campos obligatorios para Django Admin y permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"
