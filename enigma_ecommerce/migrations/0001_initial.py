# Generated by Django 5.0.1 on 2024-01-16 17:51

import django.db.models.deletion
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import migrations, models


def create_groups(apps, schema_editor):
    Group.objects.create(name='Customers')
    Group.objects.create(name='Sellers')

    customers_group = Group.objects.get(name='Customers')
    sellers_group = Group.objects.get(name='Sellers')

    view_product_permission = Permission.objects.get(codename='view_product')
    customers_group.permissions.add(view_product_permission)

    modify_product_permission = Permission.objects.get(codename='modify_product')
    add_product_permission = Permission.objects.get(codename='add_product')
    delete_product_permission = Permission.objects.get(codename='delete_product')

    sellers_group.permissions.add(
        add_product_permission, modify_product_permission, delete_product_permission
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='product_images')),
                (
                    'image_thumbnail',
                    models.ImageField(upload_to='product_images_thumbnails'),
                ),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('delivery_address', models.TextField(max_length=255)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('payment_due_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('quantity', models.PositiveIntegerField()),
                (
                    'order',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='enigma_ecommerce.order',
                    ),
                ),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='enigma_ecommerce.product',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(
                through='enigma_ecommerce.OrderItem', to='enigma_ecommerce.product'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='enigma_ecommerce.productcategory',
            ),
        ),
    ]
