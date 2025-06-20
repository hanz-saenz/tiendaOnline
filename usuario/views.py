from django.shortcuts import render, redirect
from django.contrib.auth  import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import PerfilUsuario
# Create your views here.


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