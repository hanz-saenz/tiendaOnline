from django.contrib import admin
from .models import Categoria, Producto, Proveedor, Imagen, Carrito, ItemCarrito


class ProductoAdmin(admin.ModelAdmin):

    list_display = ('id',"nombre", 'precio')
    search_fields = ('nombre', 'precio')
    list_filter = ('categorias', 'proveedor')
    list_editable = ('nombre','precio',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion',)
    ordering = ('-precio',)
    date_hierarchy = 'fecha_creacion'


admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Proveedor)
admin.site.register(Imagen)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
