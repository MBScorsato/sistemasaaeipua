# Generated by Django 4.2.3 on 2023-07-10 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina_inicial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclame',
            name='resposta',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
