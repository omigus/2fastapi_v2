# Generated by Django 3.0.6 on 2020-09-16 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrationCore', '0007_auto_20200916_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='created_on',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
