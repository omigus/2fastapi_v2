# Generated by Django 3.0.6 on 2020-09-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrationCore', '0014_auto_20200921_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_token',
            name='system_token',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]