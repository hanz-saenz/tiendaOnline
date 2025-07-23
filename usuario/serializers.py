from rest_framework import serializers
from .models import PerfilUsuario
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PerfilUsuario
        fields = ('id', 'user', 'telefono', 'direccion', 'fecha_nacimiento')