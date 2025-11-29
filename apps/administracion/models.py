from django.db import models
from apps.usuarios.models import Usuario

class Admin(Usuario):
    class Meta:
        proxy = True
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"


class SuperAdmin(Usuario):
    class Meta:
        proxy = True
        verbose_name = "SuperAdministrador"
        verbose_name_plural = "SuperAdministradores"
