# Generated by Django 4.1 on 2023-12-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
