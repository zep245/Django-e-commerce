# Generated by Django 4.2.3 on 2023-12-23 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Category'},
        ),
    ]
