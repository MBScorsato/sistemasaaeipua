# Generated by Django 4.2.10 on 2024-02-17 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0002_informacoes_analises_basicas_interna_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco_reservatorio_temporal',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Informacoes_Analises_Basicas_Interna',
        ),
        migrations.DeleteModel(
            name='Banco_Reservatorio_temporal',
        ),
    ]
