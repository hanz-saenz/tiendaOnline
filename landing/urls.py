from django.urls import path

from .views import index, IndexView, contacto_form

urlpatterns = [
    path('', index, name='index'),
    path('index/', IndexView.as_view(), name='index-class'),
    path('contacto/', contacto_form, name='contacto'),
]