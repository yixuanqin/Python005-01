# Generated by Django 2.2.13 on 2021-01-24 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210123_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='reci_mobile',
            field=models.CharField(default='', help_text='联系电话', max_length=11, verbose_name='联系电话'),
        ),
    ]
