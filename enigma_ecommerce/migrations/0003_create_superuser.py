# Generated by Django 5.0.1 on 2024-01-16 18:06

from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    User.objects.create_superuser('admin_enigma', 'admin@example.com', 'adminpassword')


class Migration(migrations.Migration):
    dependencies = [
        ('enigma_ecommerce', '0002_create_groups'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
