# Generated by Django 3.0.3 on 2020-09-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrationCore', '0002_auto_20200912_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='admin_password',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
