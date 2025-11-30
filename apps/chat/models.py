from django.db import models
from usuarios.models import Usuario   # Ajustar al nombre real

class Conversacion(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conversaciones_paciente")
    admin = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="conversaciones_admin")
    estado = models.CharField(max_length=20, default="abierta")
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conv #{self.id} - Paciente {self.paciente_id}"
    

class MensajeChat(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensajes_enviados")
    receptor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="mensajes_recibidos")
    emisor_tipo = models.CharField(max_length=20)
    receptor_tipo = models.CharField(max_length=20, null=True, blank=True)
    mensaje = models.TextField()

    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.fecha_envio}] {self.emisor_id} → {self.receptor_id}"
