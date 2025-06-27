from rest_framework import serializers

from .models import Marca, Categoria, Producto, Proveedor


#serializer para Categorias

class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['id', 'nombre']



class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ['id', 'nombre']

class MarcaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marca
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()
    categorias = CategoriaSerializer(many=True)
    marca = MarcaSerializer()


    class Meta:
        model = Producto
        fields = '__all__'

    def create(self, validated_data):

        categorias_list = validated_data.pop('categorias', [])
        proveedor_data = validated_data.pop('proveedor', {})
        marca_data = validated_data.pop('marca', {})
        nombre = validated_data.pop('nombre', '')
        precio = validated_data.pop('precio', '')
        stock = validated_data.pop('stock', '')
        descripcion = validated_data.pop('descripcion', '')

        marca=Marca.objects.get(nombre=marca_data['nombre'])
        proveedor = Proveedor.objects.get(nombre=proveedor_data['nombre'])
        categorias = Categoria.objects.filter(nombre__in=[categoria['nombre'] for categoria in categorias_list])

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            marca=marca,
            proveedor=proveedor,
        )

        for categoria in categorias:
            producto.categorias.add(categoria)

        return producto
    
    def update(self, instance, validated_data):
        categorias_list = validated_data.pop('categorias', [])
        proveedor_data = validated_data.pop('proveedor', {})
        marca_data = validated_data.pop('marca', {})
        nombre = validated_data.pop('nombre', '')
        precio = validated_data.pop('precio', '')
        stock = validated_data.pop('stock', '')
        descripcion = validated_data.pop('descripcion', '')

        instance.nombre = nombre
        instance.precio = precio
        instance.stock = stock
        instance.descripcion = descripcion
        instance.save()

        for categoria in categorias_list:
            instance.categorias.add(categoria)

        return instance
