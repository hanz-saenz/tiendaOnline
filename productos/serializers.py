from rest_framework import serializers

from .models import Marca, Categoria, Producto, Proveedor, Imagen


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


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ('id', 'imagen','producto', 'es_principal')

class ProductoViewSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    categorias_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Categoria.objects.all(),
        source='categorias', 
        write_only=True
    )
    
    proveedor = ProveedorSerializer(read_only=True)
    proveedor_id = serializers.PrimaryKeyRelatedField(
        queryset=Proveedor.objects.all(),
        source='proveedor', 
        write_only=True
    )
    
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(),
        source='marca', 
        write_only=True
    )
    
    imagenes = ImagenSerializer(many=True, read_only=True)
    imagenes_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    imagen_principal = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Producto
        fields = (
            'id', 'nombre', 'precio', 'stock', 'descripcion', 
            'categorias', 'categorias_ids', 'proveedor', 'proveedor_id', 
            'marca', 'marca_id', 'imagenes', 'imagenes_files', 'imagen_principal'
        )

    def create(self, validated_data):
        categorias_ids = validated_data.pop('categorias_ids', [])
        proveedor = validated_data.pop('proveedor')
        marca = validated_data.pop('marca')
        imagenes_files = validated_data.pop('imagenes_files', [])
        imagen_principal = validated_data.pop('imagen_principal', None)

        producto = Producto.objects.create(
            nombre=validated_data.get('nombre'),
            descripcion=validated_data.get('descripcion'),
            precio=validated_data.get('precio'),
            stock=validated_data.get('stock'),
            activo=validated_data.get('activo', True),
            proveedor=proveedor,
            marca=marca
        )
        producto.categorias.set(categorias_ids)

        if imagen_principal:
            Imagen.objects.create(
                producto=producto,
                imagen=imagen_principal,
                es_principal=True
            )
        for imagen_file in imagenes_files:
            Imagen.objects.create(
                producto=producto,
                imagen=imagen_file,
                es_principal=False
            )

        return producto
    
    def update(self, instance, validated_data):
        categorias_ids = validated_data.pop('categorias_ids', [])
        proveedor = validated_data.pop('proveedor', instance.proveedor)
        marca = validated_data.pop('marca', instance.marca)
        imagenes_files = validated_data.pop('imagenes_files', [])
        imagen_principal = validated_data.pop('imagen_principal', None)

        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.activo = validated_data.get('activo', instance.activo)
        instance.proveedor = proveedor
        instance.marca = marca
        instance.save()

        instance.categorias.set(categorias_ids)

        if imagen_principal:
            imagen_principal_existente = instance.imagenes.filter(es_principal=True).first()
            if imagen_principal_existente:
                imagen_principal_existente.imagen = imagen_principal
                imagen_principal_existente.save()
            else:
                Imagen.objects.create(
                    producto=instance,
                    imagen=imagen_principal,
                    es_principal=True
                )

        for imagen_file in imagenes_files:
            Imagen.objects.create(
                producto=instance,
                imagen=imagen_file,
                es_principal=False
            )

        return instance