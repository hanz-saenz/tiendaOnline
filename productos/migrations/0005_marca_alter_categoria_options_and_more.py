# Generated by Django 5.2.3 on 2025-06-25 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_merge_20250624_2001'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Marca',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('nombre', models.CharField(max_length=100)),
        #         ('descripcion', models.TextField(blank=True, null=True)),
        #         ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
        #         ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
        #     ],
        #     options={
        #         'verbose_name': 'Marca',
        #         'verbose_name_plural': 'Marcas',
        #     },
        # ),
        # migrations.AlterModelOptions(
        #     name='categoria',
        #     options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        # ),
        # migrations.AlterModelOptions(
        #     name='proveedor',
        #     options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        # ),
        # migrations.AddField(
        #     model_name='categoria',
        #     name='descripcion',
        #     field=models.TextField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='producto',
        #     name='activo',
        #     field=models.BooleanField(default=True),
        # ),
        # migrations.AddField(
        #     model_name='producto',
        #     name='descripcion',
        #     field=models.TextField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='producto',
        #     name='stock',
        #     field=models.PositiveIntegerField(default=1),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='proveedor',
        #     name='descripcion',
        #     field=models.TextField(blank=True, null=True),
        # ),
        # migrations.AlterField(
        #     model_name='categoria',
        #     name='fecha_actualizacion',
        #     field=models.DateTimeField(auto_now=True),
        # ),
        # migrations.AlterField(
        #     model_name='categoria',
        #     name='fecha_creacion',
        #     field=models.DateTimeField(auto_now_add=True),
        # ),
        # migrations.AlterField(
        #     model_name='categoria',
        #     name='nombre',
        #     field=models.CharField(max_length=100),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='categorias',
        #     field=models.ManyToManyField(to='productos.categoria'),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='fecha_actualizacion',
        #     field=models.DateTimeField(auto_now=True),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='fecha_creacion',
        #     field=models.DateTimeField(auto_now_add=True),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='nombre',
        #     field=models.CharField(max_length=100),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='precio',
        #     field=models.DecimalField(decimal_places=2, max_digits=10),
        # ),
        # migrations.AlterField(
        #     model_name='producto',
        #     name='proveedor',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='productos.proveedor'),
        #     preserve_default=False,
        # ),
        # migrations.AlterField(
        #     model_name='proveedor',
        #     name='fecha_actualizacion',
        #     field=models.DateTimeField(auto_now=True),
        # ),
        # migrations.AlterField(
        #     model_name='proveedor',
        #     name='fecha_creacion',
        #     field=models.DateTimeField(auto_now_add=True),
        # ),
        # migrations.AlterField(
        #     model_name='proveedor',
        #     name='nombre',
        #     field=models.CharField(max_length=100),
        # ),
        # migrations.AddField(
        #     model_name='producto',
        #     name='marca',
        #     field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='productos.marca'),
        #     preserve_default=False,
        # ),
    ]
