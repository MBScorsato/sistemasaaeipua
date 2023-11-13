from django.db import models


class Senha(models.Model):
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.senha


class Numero_Media(models.Model):
    n = models.IntegerField()

    def __str__(self):
        return str(self.n)