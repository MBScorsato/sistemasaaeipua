# Generated by Django 4.2.3 on 2023-07-30 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0019_tabela_estoque_cal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabela_estoque_cal',
            name='resultado_final',
            field=models.IntegerField(default=0),
        ),
    ]
