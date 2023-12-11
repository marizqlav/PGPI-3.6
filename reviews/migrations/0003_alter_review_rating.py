# Generated by Django 4.1 on 2023-12-06 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
