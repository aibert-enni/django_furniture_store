# Generated by Django 5.1.1 on 2024-09-29 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_rename_categoty_products_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ('id',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
