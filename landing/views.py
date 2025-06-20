from django.shortcuts import render
from django.views.generic import TemplateView
from productos.models import Categoria

# Create your views here.
def index(request):

    lista_categorias = Categoria.objects.all()

    context = {
        'categorias': lista_categorias
    }
    return render(request, 'index.html', context)

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
        


