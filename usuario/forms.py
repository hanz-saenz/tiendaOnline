from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroUsuariotForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese un correo electrónico válido.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


#editar ferfil de Usuario

class EditarPerfil(forms.ModelForm):
    nombre = forms.CharField(max_length=20, required=True, help_text='Requerido. Ingrese su primer nombre.')
    apellido = forms.CharField(max_length=20, required=True, help_text='Requerido. Ingrese su apellido.')

    class Meta:
        model = PerfilUsuario
        fields = ('foto_perfil', 'telefono', 'direccion')

        