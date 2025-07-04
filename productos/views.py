from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .decorators import es_superuser

# @login_required(login_url='login')
# @permission_required('productos.view_producto', login_url='login')

from django.core.paginator import Paginator
from django.core.cache import cache
import logging

logger_productos = logging.getLogger(__name__)


@user_passes_test(es_superuser, login_url='index')
def lista_productos(request):
    pagina = request.GET.get('page')

    cache_key = f"productos_{pagina}"

    productos = cache.get(cache_key)
    logger_productos.debug(f"Productos obtenidos de la cache: {productos}")
    if not productos:
        productos = Producto.objects.filter(activo=True).select_related('proveedor', 'marca').prefetch_related('categorias')
        for producto in productos:
            imagen_principal = Imagen.objects.filter(producto=producto, es_principal=True).first()
            if imagen_principal:
                producto.imagen = imagen_principal.imagen
        paginador = Paginator(productos, 3)
        productos = paginador.get_page(pagina)

        cache.set(cache_key, productos, 60 * 15)
    variable = "hola"
    try:
        print(variable+4)
    except Exception as e:
        logger_productos.error(f"Error al acceder a la variable: {e}")

    context = {
        'productos': productos,
        # 'page_obj': paginador
    }

    return render(request, 'productos/lista_productos.html', context)






# vista categorias froms.Form

from .forms import *

def nueva_categoria(request):
    if request.method== 'POST':
        formulario = CategoriaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            descripcion = formulario.cleaned_data['descripcion']
            print(f"Nombre: {nombre}, Descripcion: {descripcion}")
            formulario.save()
            return render(request, 'index.html')
    else:
        formulario = CategoriaForm()

    contextos = {
        'formulario': formulario
    }
    return render(request, 'categorias/nueva_categoria.html', contextos)

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class CategoriasView(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    template_name = 'categorias/lista_categorias.html'
    permission_required = ('productos.view_categoria', 'productos.add_categoria', 'productos.change_categoria', 'productos.delete_categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
       
        context['categorias'] = categorias
        return context
    

class CrearCategoriaView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias')
    template_name = 'categorias/nueva_categoria.html'
    #fields = ['nombre', 'descripcion']

class ActualizarCategoriaView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias')
    template_name = 'categorias/nueva_categoria.html'
    #fields = ['nombre', 'descripcion']

class EliminarCategoriaView(DeleteView):
    model = Categoria
    success_url = reverse_lazy('categorias')
    template_name = 'categorias/eliminar_categoria.html'


class MarcaView(TemplateView):
    template_name = 'marcas/lista_marcas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        marcas = Marca.objects.all()
       
        context['marcas'] = marcas
        return context
    
class CrearMarcaView(CreateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy('marcas')
    template_name = 'marcas/nueva_marca.html'
    #fields = ['nombre', 'descripcion']


class ActualizarMarcaView(UpdateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy('marcas')
    template_name = 'marcas/nueva_marca.html'
    #fields = ['nombre', 'descripcion']

class EliminarMarcaView(DeleteView):
    model = Marca
    success_url = reverse_lazy('marcas')
    template_name = 'marcas/eliminar_marca.html'

class ProveedorView(TemplateView):
    template_name = 'proveedores/lista_proveedores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proveedores = Proveedor.objects.all()
       
        context['proveedores'] = proveedores
        return context
    
class CrearProveedorView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores')
    template_name = 'proveedores/nuevo_proveedor.html'
    #fields = ['nombre', 'descripcion']

class ActualizarProveedorView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores')
    template_name = 'proveedores/nuevo_proveedor.html'
    #fields = ['nombre', 'descripcion']

class EliminarProveedorView(DeleteView):
    model = Proveedor
    success_url = reverse_lazy('proveedores')
    template_name = 'proveedores/eliminar_proveedor.html'


class ProductosView(TemplateView):
    template_name = 'productos/lista_productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = Producto.objects.filter(activo=True)
        for producto in productos:
            imagen_principal = Imagen.objects.filter(producto=producto, es_principal=True).first()
            if imagen_principal:
                producto.imagen = imagen_principal.imagen
        
        context['productos'] = productos
        return context
    
class CrearProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('productos')
    template_name = 'productos/nuevo_producto.html'
    #fields = ['nombre', 'descripcion']

    def post(self, request, *args, **kwargs):
        print('self.request post', request)
        print('request.FILES post', request.FILES)

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            print('Formulario válido', form.cleaned_data)
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            # categoria = form.cleaned_data['categorias']
            imagen = form.cleaned_data['imagen']
            stock = form.cleaned_data['stock']
            proveedor = form.cleaned_data['proveedor']
            marca = form.cleaned_data['marca']



        # if 'imagen' in request.FILES:
        #     imagenes = request.FILES.getlist('imagen')
        #     print('imagenes', imagenes)
        #     for imagen in imagenes:
        #         print('imagen', imagen)
        #         Imagen.objects.create(producto=self.object, imagen=imagen, es_principal=True)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        if 'imagen' in self.request.FILES:
            imagenes = self.request.FILES.getlist('imagen')
            print('imagenes', imagenes)
            # Si hay imágenes, las guardamos
            for imagen in imagenes:
                print('imagen', imagen)
                Imagen.objects.create(producto=self.object, imagen=imagen, es_principal=True)

        return super().form_valid(form)


class ActualizarProductoView(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('productos')
    template_name = 'productos/nuevo_producto.html'
    #fields = ['nombre', 'descripcion']

    def form_valid(self, form):
        self.object = form.save()

        if 'imagen' in self.request.FILES:
            imagenes = self.request.FILES.getlist('imagen')
            print('imagenes', imagenes)
            # Si hay imágenes, las guardamos
            for imagen in imagenes:
                print('imagen', imagen)
                Imagen.objects.create(producto=self.object, imagen=imagen, es_principal=True)

        return super().form_valid(form)

class EliminarProductoView(DeleteView):
    model = Producto
    success_url = reverse_lazy('productos')
    template_name = 'productos/eliminar_producto.html'



##################################################################################
######################## DRF #####################################################
##################################################################################




from rest_framework.views import APIView
from .serializers import CategoriaSerializer, ProductoSerializer
from rest_framework.response import Response
from rest_framework import status

class CategoriasApiView(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        print(type(categorias))
        serializer = CategoriaSerializer(categorias, many=True)
        print(type(serializer.data))
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serialializer = CategoriaSerializer(data=request.data)
        if serialializer.is_valid():
            serialializer.save()
            return Response(serialializer.data, status=status.HTTP_201_CREATED)
        return Response(serialializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        try:
            categoria = Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        categoria = Categoria.objects.get(pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

class ActualizarCategoriaApiView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductosApiView(APIView):
    def get(self, request, format=None):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def ajax_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/productos_ajax.html', {'categorias': categorias})

from .tasks import estado_tarea
from django.http import JsonResponse
from celery.result import AsyncResult   

def generar_tare(request):
    tarea= estado_tarea.delay(10)

    context = {
        'tarea_id': tarea.id
        }
    return render(request, 'resutado_tareas.html', context)

def consultar_tarea(request, tarea_id):
    tarea = AsyncResult(tarea_id)
    context = {
        'id': tarea.id,
        'estado': tarea.status,
        'resultado': tarea.result if tarea.ready() else None,
    }
    return JsonResponse(context)