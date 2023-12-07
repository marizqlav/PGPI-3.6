# Generated by Django 4.2.7 on 2023-12-07 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_order_status_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('EA', 'En Almacen'), ('P', 'Procesando'), ('EC', 'En Camino'), ('E', 'Entregado')], default='EA', max_length=2),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('EA', 'En Almacen'), ('P', 'Procesando'), ('EC', 'En Camino'), ('E', 'Entregado')], default='EA', max_length=2),
        ),
    ]