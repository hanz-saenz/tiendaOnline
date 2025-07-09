from modeltranslation.translator import register, TranslationOptions, translator
from .models import Producto, Categoria, Proveedor, Marca


@register(Producto)
class ProductosTraduccion(TranslationOptions):
    fields = ('nombre', 'descripcion')

@register(Categoria)
class CategoriaTraduccion(TranslationOptions):
    fields = ('nombre', 'descripcion')

# @register(Proveedor)
# class ProveedorTraduccion(TranslationOptions):
#     fields = ('nombre', 'descripcion')

# # @register(Marca)
# class MarcaTraduccion(TranslationOptions):
#     fields = ('nombre', 'descripcion')


# translator.register(Proveedor, ProveedorTraduccion)
# translator.register(Marca,MarcaTraduccion)