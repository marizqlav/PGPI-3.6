# Generated by Django 4.2.7 on 2023-12-05 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_order_tracking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
