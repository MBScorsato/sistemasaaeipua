import self as self
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Senha(models.Model):
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.senha


class Numero_Media(models.Model):

    n = models.IntegerField()

    def __str__(self):
        return str(self.n)


class Controle_Operacional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    pre_cloro = models.FloatField()
    cloro_esstacao = models.FloatField()
    turbidez_estacao = models.FloatField()

    relatorio = models.TextField()

    def __str__(self):
        # Obtendo o nome de usuário do usuário relacionado
        nome_usuario = self.usuario.username

        return f"{nome_usuario}"