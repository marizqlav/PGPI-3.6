# Generated by Django 3.0 on 2023-12-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0004_claim_admin_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
