from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from productos.models import Categoria
from .forms import ContactoForm

from django.core.mail import send_mail
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
        

from django.conf import settings
def contacto_form(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()

            # send_mail(
            #     subject=f"Contacto {form.cleaned_data['nombre']}",
            #     message=form.cleaned_data['mensaje'],
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[settings.EMAIL_HOST_USER, form.cleaned_data['email']],
            #     fail_silently=False
            # )
            return redirect('contacto')
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})