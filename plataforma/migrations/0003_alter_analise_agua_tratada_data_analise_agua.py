# Generated by Django 4.2.3 on 2023-07-25 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_alter_analise_agua_tratada_data_analise_agua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analise_agua_tratada',
            name='data_analise_agua',
            field=models.DateTimeField(),
        ),
    ]
