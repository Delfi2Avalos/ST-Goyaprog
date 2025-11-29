from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, contrasena=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    TIPO_CHOICES = [
        ("paciente", "Paciente"),
        ("medico", "Médico"),
        ("admin", "Admin"),
        ("superadmin", "SuperAdmin"),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    obra_social = models.CharField(max_length=100, null=True, blank=True)
    detalles_extras = models.TextField(null=True, blank=True)
    registrado_en = models.DateTimeField(auto_now_add=True)
    ultima_conexion = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "tipo"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
