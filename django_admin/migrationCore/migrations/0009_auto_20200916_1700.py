# Generated by Django 3.0.6 on 2020-09-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrationCore', '0008_auto_20200916_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(blank=True, max_length=180, null=True, unique=True),
        ),
    ]
