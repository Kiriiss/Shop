# Generated by Django 4.1.7 on 2023-02-25 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_user_order_initiator_order_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]