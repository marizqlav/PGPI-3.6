# Generated by Django 4.2.7 on 2023-12-02 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='refund_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='refund_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PL', 'Placed'), ('PR', 'Processing'), ('SH', 'Shipped'), ('DE', 'Delivered')], default='PL', max_length=2),
        ),
        migrations.AddField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('PL', 'Placed'), ('PR', 'Processing'), ('SH', 'Shipped'), ('DE', 'Delivered')], default='PL', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='maker',
            field=models.CharField(choices=[('Berria', 'Berria'), ('BH', 'BH'), ('CBK', 'CBK'), ('Goka', 'Goka'), ('Massi', 'Massi'), ('Megamo', 'Megamo'), ('MMR ', 'MMR '), ('Monty', 'Monty'), ('MSC', 'MSC'), ('Orbea', 'Orbea'), ('Vitoria', 'Vitoria'), ('Unno', 'Unno')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Cuadro', 'Cuadro'), ('Manillar', 'Manillar'), ('Sillin', 'Sillin'), ('Camara', 'Camara'), ('Rueda', 'Rueda'), ('Freno', 'Freno'), ('Pedal', 'Pedal'), ('Cambios', 'Cambios')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
