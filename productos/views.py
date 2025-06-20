from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .decorators import es_superuser

# @login_required(login_url='login')
# @permission_required('productos.view_producto', login_url='login')

@user_passes_test(es_superuser, login_url='index')
def lista_productos(request):
    productos = Producto.objects.filter(activo=True)


    for producto in productos:
        imagen_principal = Imagen.objects.filter(producto=producto, es_principal=True).first()
        if imagen_principal:
            producto.imagen = imagen_principal.imagen

    context = {
        'productos': productos
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