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


class Fluor_diario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Campo para relacionar com o usuário
    fluor = models.FloatField()
    data = models.DateTimeField(default=timezone.now)
    relatorio = models.TextField()

    def __str__(self):

        # Obtendo o nome de usuário do usuário relacionado
        nome_usuario = self.usuario.username

        return f"{nome_usuario}"
