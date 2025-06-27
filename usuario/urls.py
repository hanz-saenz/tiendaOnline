from django.urls import path
from .views import *

urlpatterns = [
    path('registro-class/', RegistroUsuarioView.as_view(), name='registro-class'),
    path('registro/', registro_view, name='registro'),
    path('consultaer-perfil/', consultaer_perfil, name='consultaer_perfil'),
    path('asignar-permisos/<int:user_id>', AsignarPermisosView.as_view(), name='asignar_permisos'),
    path('crear-grupo/', CrearGrupoView.as_view(), name='crear_grupo'),
    path('asignar-grupos-usuario/<int:user_id>', AsignarGruposUsuario.as_view(), name='asignar_grupos'),
    path('lista-usuarios/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('editar-usuario/', editar_perfil, name='editar_usuario'),

    #drf
    path('generar-toke/', generar_token, name='generar_token'),
    path('login/', LoginApiView.as_view(), name='login-drf'),
]
