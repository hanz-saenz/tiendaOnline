from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuariotForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese un correo electrónico válido.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        