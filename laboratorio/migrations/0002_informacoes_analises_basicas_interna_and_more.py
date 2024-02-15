# Generated by Django 4.2.10 on 2024-02-14 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Informacoes_Analises_Basicas_Interna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('informativo', models.TextField()),
            ],
            options={
                'verbose_name': 'Informe para Análises básicas internas',
                'verbose_name_plural': 'Informe para Análises básicas internas',
            },
        ),
        migrations.AlterModelOptions(
            name='anotacoes',
            options={'verbose_name': 'Anotações', 'verbose_name_plural': 'Anotações'},
        ),
        migrations.AlterModelOptions(
            name='cadastro_reservatorio',
            options={'verbose_name': 'Cadastro Reservatório', 'verbose_name_plural': 'Cadastro Reservatório'},
        ),
        migrations.AlterModelOptions(
            name='controle_operacional',
            options={'verbose_name': 'Controle Operacional', 'verbose_name_plural': 'Controle Operacional'},
        ),
        migrations.CreateModel(
            name='Banco_Reservatorio_temporal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('rua', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=100)),
                ('cloro', models.CharField(max_length=100)),
                ('fluor', models.CharField(max_length=100)),
                ('ph', models.CharField(max_length=100)),
                ('turbidez', models.CharField(max_length=100)),
                ('analise', models.CharField(max_length=50)),
                ('data_agora', models.DateTimeField(default=django.utils.timezone.now)),
                ('observacao', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Relatorio',
                'verbose_name_plural': 'Relatorio',
            },
        ),
    ]
