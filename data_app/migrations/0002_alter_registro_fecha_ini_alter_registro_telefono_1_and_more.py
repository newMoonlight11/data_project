# Generated by Django 5.2.3 on 2025-06-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='fecha_ini',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='telefono_1',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registro',
            name='telefono_2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registro',
            name='telefono_3',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
