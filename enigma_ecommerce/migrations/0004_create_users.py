from django.db import migrations
from django.contrib.auth.models import User, Group


def create_users_and_assign_to_groups(apps, schema_editor):
    sellers_group, _ = Group.objects.get_or_create(name='Sellers')
    customers_group, _ = Group.objects.get_or_create(name='Customers')

    user_seller = User.objects.create_user(
        username='seller_user',
        password='password',
        email='seller@example.com',
    )
    user_customer = User.objects.create_user(
        username='customer_user',
        password='password',
        email='customer@example.com',
    )

    user_seller.groups.add(sellers_group)
    user_customer.groups.add(customers_group)


class Migration(migrations.Migration):
    dependencies = [
        ('enigma_ecommerce', '0002_create_groups'),
        ('enigma_ecommerce', '0003_create_superuser')
    ]

    operations = [
        migrations.RunPython(create_users_and_assign_to_groups),
    ]
