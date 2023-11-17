from django.db import models


# criar uma tabela auxiliar para tudo postado seja nela
class Reclame(models.Model):
    mensagem = models.TextField()
    nome = models.CharField(max_length=100)
    rua = models.CharField(max_length=50)
    email_ou_tel = models.CharField(max_length=30)
    boolean = models.BooleanField(default=False)
    resposta = models.CharField(max_length=300)

    def __str__(self):
        return self.rua


class Aviso(models.Model):
    foto = models.ImageField(upload_to='aviso_images')
    titulo = models.CharField(max_length=50)
    texto = models.TextField()

    def __str__(self):
        return self.titulo


class Contato(models.Model):
    cidade_estado = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"Cidade e contato da estação - ETA"
