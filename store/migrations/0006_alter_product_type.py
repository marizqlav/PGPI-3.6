# Generated by Django 4.1 on 2023-12-01 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Cuadro', 'Cuadro'), ('Manillar', 'Manillar'), ('Sillin', 'Sillin'), ('Camara', 'Camara'), ('Rueda', 'Rueda'), ('Freno', 'Freno'), ('Pedal', 'Pedal'), ('Cambios', 'Cambios')], max_length=200, null=True),
        ),
    ]
