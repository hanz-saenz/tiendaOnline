from django.urls import path

from .views import index, IndexView

urlpatterns = [
    path('', index, name='index'),
    path('index/', IndexView.as_view(), name='index-class'),
]