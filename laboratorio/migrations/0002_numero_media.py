# Generated by Django 4.2.3 on 2023-10-31 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Numero_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.IntegerField(default=12)),
            ],
        ),
    ]
