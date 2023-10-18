from django.db import models
from django.utils import timezone


class EtaMidia(models.Model):
    titulo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='Eta_foto')
    mensagem = models.TextField()
    data_criacao = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.data_criacao}"

