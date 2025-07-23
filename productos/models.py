from django.db import models
from deep_translator import GoogleTranslator
# Create your models here.
# Categorias
# Proveedor
# Marca
# Productos

def traducir_texto(texto, entrada='es', salida='en'):
    try:
        traduccion = GoogleTranslator(source=entrada, target=salida).translate(texto)
        return traduccion
    except Exception as e:
        print(f"Error al traducir el texto: {e}")
        return texto

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def save(self, *args, **kwargs):
        if not self.nombre_en:
            self.nombre_en = traducir_texto(self.nombre, entrada='es', salida='en')
        if not self.nombre_fr:
            self.nombre_fr = traducir_texto(self.nombre, entrada='es', salida='fr')
        if not self.descripcion_en:
            self.descripcion_en = traducir_texto(self.descripcion, entrada='es', salida='en')
        if not self.descripcion_fr:
            self.descripcion_fr = traducir_texto(self.descripcion, entrada='es', salida='fr')
        super().save(*args, **kwargs)
        

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    categorias = models.ManyToManyField(Categoria)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.nombre_en:
            self.nombre_en = traducir_texto(self.nombre, entrada='es', salida='en')
        if not self.nombre_fr:
            self.nombre_fr = traducir_texto(self.nombre, entrada='es', salida='fr')
        if not self.descripcion_en:
            self.descripcion_en = traducir_texto(self.descripcion, entrada='es', salida='en')
        if not self.descripcion_fr:
            self.descripcion_fr = traducir_texto(self.descripcion, entrada='es', salida='fr')
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Imagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    es_principal = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Imagen de {self.producto}"
    
    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'