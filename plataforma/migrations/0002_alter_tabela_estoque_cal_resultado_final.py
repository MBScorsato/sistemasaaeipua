# Generated by Django 4.2.10 on 2024-02-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabela_estoque_cal',
            name='resultado_final',
            field=models.IntegerField(),
        ),
    ]