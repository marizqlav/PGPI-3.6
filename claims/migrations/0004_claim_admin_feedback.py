# Generated by Django 4.1 on 2023-12-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0003_alter_claim_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='admin_feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]
