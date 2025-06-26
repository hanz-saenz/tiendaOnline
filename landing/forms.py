from django import forms

from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje', 'telefono']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control formulario', 'required':True  }),
            'email': forms.EmailInput(attrs={'class': 'form-control formulario', 'required':True}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control formulario', 'required':True}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control formulario', 'required':True}),
        }