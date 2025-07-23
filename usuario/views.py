from django.shortcuts import render, redirect
from django.contrib.auth  import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import PerfilUsuario
# Create your views here.
from .forms import EditarPerfil

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')
        
    return render(request, 'usuarios/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'Has cerrado sesión correctamente')
    else:
        messages.error(request, 'No has iniciado sesión')
    return redirect('login')

from .forms import RegistroUsuariotForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy


class RegistroUsuarioView(CreateView):
    model = User
    form_class = RegistroUsuariotForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuariotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('login')
        else:
            messages.error(request, 'Error al registrar el usuario')
    else:
        form = RegistroUsuariotForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def consultaer_perfil(request):

    datos_usuario = PerfilUsuario.objects.get(user=request.user)

    print(datos_usuario.user.username)
    print(datos_usuario.user.email)
    print(datos_usuario.direccion)

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

#asignacion de permisos
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.change_permission', raise_exception=True), name='dispatch')
class AsignarPermisosView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        permisos = Permission.objects.all()

        context = {
            'user': user,
            'permisos': permisos
        }

        return render(request, 'usuarios/asignar_permisos.html', context)
    
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        print('user', user)
        permisos_asignados = request.POST.getlist('permisos')
        print('permisos_asignados', permisos_asignados)
        print('user.user_permissions', user.user_permissions)
        user.user_permissions.clear()
        print('user.user_permissions limpios', user.user_permissions)

        for permiso in permisos_asignados:
            print('permiso', permiso)
            permiso_obje = Permission.objects.get(id=permiso)
            print('permiso_obje', permiso_obje)
            user.user_permissions.add(permiso_obje)
            
        print('user.user_permissions asignados', user.user_permissions.all())
        return redirect('lista_usuarios')


# Creaion de grupos

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.add_group', raise_exception=True), name='dispatch')
class CrearGrupoView(View):
    def get(self, request):
        context = {
            'permisos': Permission.objects.all(),
        }

        return render(request, 'usuarios/crear_grupo.html', context)
    
    def post(self, request):
        nombre_grupo = request.POST.get('nombre_grupo')
        print('nombre_grupo', nombre_grupo)
        permisos_asignados = request.POST.getlist('permisos')
        print('permisos_asignados', permisos_asignados)

        if Group.objects.filter(name=nombre_grupo).exists():
            messages.error(request, 'El grupo ya existe')
            return redirect('lista_usuarios')
        

        grupo = Group.objects.create(name=nombre_grupo)
        
        for permiso in permisos_asignados:
            print('permiso', permiso)
            permiso_obje = Permission.objects.get(id=permiso)
            print('permiso_obje', permiso_obje)
            grupo.permissions.add(permiso_obje)
        messages.success(request, 'Grupo creado correctamente')
        return redirect('lista_usuarios')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.change_user', raise_exception=True), name='dispatch')
class AsignarGruposUsuario(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        grupos = Group.objects.all()

        context = {
            'user': user,
            'grupos': grupos
        }

        return render(request, 'usuarios/asignar_grupos.html', context)
    
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        print('user', user)
        grupos_asignados = request.POST.getlist('groups')
        print('grupos_asignados', grupos_asignados)
        print('user.groups', user.groups)
        user.groups.clear()
        print('user.groups limpios', user.groups)

        for grupo in grupos_asignados:
            print('permiso', grupo)
            grupo_obj = Group.objects.get(id=grupo)
            print('grupo_obj', grupo_obj)
            user.groups.add(grupo_obj)
            
        print('user.groups asignados', user.groups.all())
        return redirect('lista_usuarios')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.change_user', raise_exception=True), name='dispatch')
class ListaUsuariosView(View):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        context = {
            'users': users,
        }

        return render(request, 'usuarios/lista_usuarios.html', context)
    


@login_required
def editar_perfil(request):
    """
    Permite a un usuario autenticado editar su perfil.

    - Obtiene o crea el perfil asociado al usuario actual.
    - Si la petición es POST, procesa el formulario de edición:
        - Actualiza el nombre y apellido del usuario.
        - Guarda los cambios en el perfil y el usuario.
        - Muestra un mensaje de éxito y redirige a la vista de edición de usuario.
        - Si el formulario no es válido, muestra un mensaje de error.
    - Si la petición es GET, inicializa el formulario con los datos actuales del usuario y su perfil.
    - Renderiza la plantilla 'usuarios/editar_perfil.html' con el formulario y la imagen de perfil.

    Args:
        request (HttpRequest): La petición HTTP recibida.

    Returns:
        HttpResponse: Renderiza la plantilla de edición de perfil con el contexto correspondiente.
    """
    user = request.user
    print('user', user)
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = EditarPerfil(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            user.save()
            form.save()
            messages.success(request, 'Perfil editado correctamente.')
            return redirect('editar_usuario')  # Cambia 'login' por la URL deseada
        else:
            messages.error(request, 'Error al editar el perfil. Por favor, corrige los errores.')
    else:
        initial_data = {
            'nombre': user.first_name,
            'apellido': user.last_name,
            'telefono': perfil.telefono,
            'direccion': perfil.direccion,
            'fecha_nacimiento': perfil.fecha_nacimiento,
            'foto_perfil': perfil.foto_perfil,
        }
        form = EditarPerfil(instance=perfil, initial=initial_data)

    context = {
        'form': form,
        'imagen': perfil.foto_perfil
    }
    return render(request, 'usuarios/editar_perfil.html', context)


###############################################################
################## DRF#########################################


from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response

def generar_token(request):
    user = request.user
    print('user', user)
    token, created = Token.objects.get_or_create(user=user)
    print('TOKEN', token.key)

    return JsonResponse({'token': token.key})
    

class LoginApiView2(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        try:

            usuario = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request=request, username=usuario, password=password)
            if user:
                auth_login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                #token de jwt
                generar_tokens = RefreshToken.for_user(user)

                return Response(
                    {
                        'status': 'success',
                        'data': {
                            'access_token': str(generar_tokens.access_token),
                            'refresh_token': str(generar_tokens),
                        },
                        'mensaje': 'Has iniciado sesión correctamente',
                    }, status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                    {
                        'status': 'error',
                        'data': None,
                        'mensaje': f'Error al iniciar sesión. Codigo de error: {e}',
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        

#####################################################################
# Estructura proyecto tienda online


## Registro de usuario APIView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class RegistroUsuarioApiView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        #status - success, error
        #data - datos del usuario - None
        #mensaje - mensaje de éxito o error
        #
        try:
            print('request.data', request.data)
            datos = request.data
            username = datos.get('username')
            password = datos.get('password')
            email = datos.get('email')

            registro = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return Response(
                {
                    'status': 'success',
                    'data': {
                        'id': registro.id,
                        'username': registro.username,
                        'email': registro.email
                    },
                    'mensaje': 'Usuario registrado correctamente',
                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'data': None,
                    'mensaje': f'Error al registrar el usuario. Codigo de error: {e}',
                }, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request=request, username=username, password=password)

            #creación del token

            if user:

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # guardar token en las cookies

                response = Response(
                    {
                        'status': 'success',
                        'data': {
                            'access_token': access_token,
                            'refresh_token': str(refresh),
                        },
                        'mensaje': 'Has iniciado sesión correctamente',
                    }, status=status.HTTP_200_OK
                )
            

                response.set_cookie(
                    key='access_token',
                    value=str(refresh.access_token),
                    httponly=True,
                    secure=False,  
                    samesite='Lax',
                    max_age=3600  
                )
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=86400  
                )

                return response
            
            return Response(
                {
                    'status': 'error',
                    'data': None,
                    'mensaje': 'Usuario o contraseña incorrectos',
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'data': None,
                    'mensaje': f'Error al iniciar sesión. Codigo de error: {e}',
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
#Validador de autenticacion

class ValidarAutenticacionAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        return Response(
            {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'mensaje': 'Usuario autenticado correctamente',
            }, status=status.HTTP_200_OK
        )

import json
from .serializers import *
class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            serializer = PerfilUsuarioSerializer(perfil)
            print('serializer.data', serializer.data)
            return Response(
                {
                    'status': 'success',
                    'data': serializer.data,
                    'mensaje': 'Perfil obtenido correctamente',
                }, status=status.HTTP_200_OK
            )
        except PerfilUsuario.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'data': None,
                    'mensaje': 'Perfil no encontrado',
                }, status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request):
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            serializer = PerfilUsuarioSerializer(perfil, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                updated_perfil = User.objects.get(id=request.user.id)
                user_request = request.data.get('user', {})

                # Si viene como string, intentar parsearlo
                if isinstance(user_request, str):
                    try:
                        user_request = json.loads(user_request)
                    except json.JSONDecodeError:
                        user_request = {}

                updated_perfil.first_name = user_request.get('first_name', updated_perfil.first_name)
                updated_perfil.last_name = user_request.get('last_name', updated_perfil.last_name)
                updated_perfil.email = user_request.get('email', updated_perfil.email)
                updated_perfil.save()
                print('guardado los datos')
                print('serializer.data', serializer.data)
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'mensaje': 'Perfil actualizado correctamente',
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'error',
                'data': serializer.errors,
                'mensaje': 'Error al actualizar el perfil',
            }, status=status.HTTP_400_BAD_REQUEST)

        except PerfilUsuario.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'data': None,
                    'mensaje': 'Perfil no encontrado',
                }, status=status.HTTP_404_NOT_FOUND
            )