# Generated by Django 5.1.5 on 2025-05-22 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articulos', '0001_initial'),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado_lotes',
            fields=[
                ('idestado_lote', models.AutoField(primary_key=True, serialize=False)),
                ('code_estado_lote', models.CharField(max_length=30, unique=True)),
                ('descripcion_estado_lote', models.CharField(max_length=30, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Estado Lote',
                'verbose_name_plural': 'Estado Lotes',
                'db_table': 'estado_lotes',
            },
        ),
        migrations.CreateModel(
            name='Lotes',
            fields=[
                ('idlote', models.AutoField(primary_key=True, serialize=False)),
                ('numero_lote', models.CharField(max_length=15, verbose_name='Número de Lote')),
                ('fecha_fabricacion', models.DateField(blank=True, null=True, verbose_name='Fecha Fabricación')),
                ('fecha_caducidad', models.DateField(blank=True, null=True, verbose_name='Fecha Caducidad')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('codigoarticulo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='articulos.articulos', verbose_name='Producto')),
                ('idestado_lote', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lotes.estado_lotes', verbose_name='Estado Lote')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
                'db_table': 'lotes',
                'ordering': ['codigoarticulo', 'fecha_caducidad'],
            },
        ),
        migrations.CreateModel(
            name='Detalle_compra_lotes',
            fields=[
                ('iddetalle_compra_lote', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
                ('iddetalle_compra', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='compras.detalle_compras', verbose_name='Detalle Compra Lote')),
                ('idlote', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lotes.lotes', verbose_name='Lote')),
            ],
            options={
                'verbose_name': 'Detalle Compra Lote',
                'verbose_name_plural': 'Detalle Compra Lotes',
                'db_table': 'detalle_compra_lotes',
            },
        ),
    ]
