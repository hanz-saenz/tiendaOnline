from django import forms
from .models import Categoria, Marca, Producto, Proveedor


class CategoriaFormForms(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre", required=True)
    descripcion = forms.CharField(max_length=100, label="Descripcion", required=True)


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control formulario'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control formulario'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control formulario'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    imagen = forms.ImageField(required=True, label="Imagen del Producto")

    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'categorias': forms.CheckboxSelectMultiple(),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
