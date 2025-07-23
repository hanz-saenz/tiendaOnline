from django.urls import path
from .views import *

urlpatterns = [
    path('lista/', lista_productos, name='lista_productos'),
    path('lista-productos/', ProductosView.as_view(), name='productos'),
    path('lista-categorias/', CategoriasView.as_view(), name='categorias'),
    path('nueva-categoria/', nueva_categoria, name='nueva_categoria'),
    path('crear-categoria/', CrearCategoriaView.as_view(), name='crear_categoria'),
    path('actualizar-categoria/<int:pk>', ActualizarCategoriaView.as_view(), name='actualizar_categoria'),
    path('eliminar-categoria/<int:pk>', EliminarCategoriaView.as_view(), name='eliminar_categoria'),

    path('lista-marcas/', MarcaView.as_view(), name='marcas'),
    path('crear-marca/', CrearMarcaView.as_view(), name='nueva_marca'),
    path('actualizar-marca/<int:pk>', ActualizarMarcaView.as_view(), name='actualizar_marca'),
    path('eliminar-marca/<int:pk>', EliminarMarcaView.as_view(), name='eliminar_marca'),

    path('lista-proveedores/', ProveedorView.as_view(), name='proveedores'),
    path('crear-proveedor/', CrearProveedorView.as_view(), name='nuevo_proveedor'),
    path('actualizar-proveedores/<int:pk>', ActualizarProveedorView.as_view(), name='actualizar_proveedor'),
    path('eliminar-proveedores/<int:pk>', EliminarProveedorView.as_view(), name='eliminar_proveedor'),

    path('crear-producto/', CrearProductoView.as_view(), name='crear_producto'),
    path('actualizar-producto/<int:pk>', ActualizarProductoView.as_view(), name='actualizar_producto'),
    path('eliminar-producto/<int:pk>', EliminarProductoView.as_view(), name='eliminar_producto'),
    path('ajax_categoria/', ajax_categoria, name='ajax_categoria'),

    #url drf
    path('api/categorias/', CategoriasApiView.as_view(), name='categorias-api'),
    path('api/productos/', ProductosApiView.as_view(), name='productos-api'),
    path('api/productos/<int:pk>/', ProductosApiView.as_view(), name='productos-api'),
    path('api/categorias/<int:pk>/', CategoriasApiView.as_view(), name='categorias-api'),

    path('api/categoria/editar_categoria/<int:pk>/', ActualizarCategoriaApiView.as_view(), name='actualizar_categoria_api'),

    path('api/productos/marcas', MarcaProductoView.as_view(), name='marcas-api'),
    path('api/productos/proveedores', ProveedorProductoView.as_view(), name='proveedor-api'),
    path('api/productos/categorias', CategoriaProductoView.as_view(), name='categorias-api'),
    path('api/productos/lista', ProductosListaView.as_view(), name='productos-lista-api'),
    path('api/productos/lista/<int:pk>/', ProductosListaView.as_view(), name='productos-lista-api-editar'),


    #generar tarea
    path('generar-tarea/', generar_tare, name='generar_tarea'),
    path('estado-tarea/<str:tarea_id>/', consultar_tarea, name='consultar_tarea'),

]