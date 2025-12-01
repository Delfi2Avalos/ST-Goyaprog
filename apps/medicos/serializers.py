from rest_framework import serializers

class TurnoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha = serializers.DateField()
    hora = serializers.TimeField()
    estado = serializers.CharField()
    detalles = serializers.CharField(allow_null=True)
    paciente_nombre = serializers.CharField()
    paciente_apellido = serializers.CharField()
    obra_social = serializers.CharField()

class HorarioMedicoSerializer(serializers.Serializer):
    dia_semana = serializers.CharField()
    hora_inicio = serializers.TimeField()
    hora_fin = serializers.TimeField()

class FormularioSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    medico_id = serializers.IntegerField()
    nombre_completo = serializers.CharField()
    contenido = serializers.CharField()
    fecha = serializers.DateTimeField(required=False)
