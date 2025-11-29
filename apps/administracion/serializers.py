from rest_framework import serializers
from apps.usuarios.models import Usuario

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
