# Generated by Django 4.1.7 on 2023-03-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='basket_history',
            field=models.JSONField(default=dict),
        ),
    ]
