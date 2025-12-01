from django.db import models
from usuarios.models import Usuario

class MedicoProxy(Usuario):
    class Meta:
        proxy = True
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
