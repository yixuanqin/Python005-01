# Generated by Django 2.2.13 on 2021-01-23 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='order_user',
            new_name='user',
        ),
    ]
