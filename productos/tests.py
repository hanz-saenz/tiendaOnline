from django.test import TestCase, Client
from .models import Categoria
from django.urls import reverse
from .forms import CategoriaForm

# Create your tests here.
class CategoriasViewsTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre='Categoria 1', 
            descripcion='Descripcion Categoria 1')

        self.lista_url = reverse('categorias')
        self.crear_url = reverse('crear_categoria')
        self.actualizar_url = reverse('actualizar_categoria', args=[self.categoria.id])
        self.eliminar_url = reverse('eliminar_categoria', args=[self.categoria.id])

        return super().setUp()
    
    def test_lista_categorias(self):
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/lista_categorias.html')
        self.assertContains(response, 'Categoria 1')

    def test_crear_categoria_view_get(self):
        response = self.client.get(self.crear_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/nueva_categoria.html')

        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertEqual(form.__class__.__name__, 'CategoriaForm')
        self.assertIn('nombre', form.fields)
        self.assertIn('descripcion', form.fields)

        # self.assertContains(response, 'Crear categoría')
    
    def test_crear_categoria_view_post(self):
        datos = {
            'nombre': 'Categoria 2',
            'descripcion': 'Descripcion Categoria 2'
        }

        response = self.client.post(self.crear_url, datos)

        # Verifica que la respuesta tenga un código de estado 302 (redirección)
        self.assertEqual(response.status_code, 302)

        # Verifica que se haya creado un nuevo objeto Categoria en la base de datos
        self.assertEqual(Categoria.objects.count(), 2)

        # Verifica que la respuesta redirija a la URL esperada
        self.assertRedirects(response, self.lista_url)

    def test_actualizar_categoria_view_get(self):
        datos = {
            'nombre': 'Categoria Actualizada',
            'descripcion': 'Descripcion Categoria Actualizada'
        }

        response = self.client.post(self.actualizar_url, datos)

        self.assertEqual(response.status_code, 302)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Categoria Actualizada')
        self.assertRedirects(response, self.lista_url)

    def test_eliminar_categoria_view_post(self):

        response = self.client.post(self.eliminar_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Categoria.objects.count(), 0)
        self.assertRedirects(response, self.lista_url)