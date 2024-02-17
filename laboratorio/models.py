from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime


class Numero_Media(models.Model):
    n = models.IntegerField()

    def __str__(self):
        return str(self.n)


class Controle_Operacional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    pre_cloro = models.FloatField()
    cloro_esstacao = models.FloatField()
    fluor = models.FloatField()
    turbidez_estacao = models.FloatField()
    relatorio = models.TextField()

    class Meta:
        verbose_name = "Controle Operacional"
        verbose_name_plural = "Controle Operacional"

    def __str__(self):
        # Obtendo o nome de usuário do usuário relacionado
        nome_usuario = self.usuario.username

        return f"{nome_usuario}"


class Cadastro_Reservatorio(models.Model):
    reservatorio_cadastrado = models.CharField(max_length=200)
    litro = models.IntegerField()

    class Meta:
        verbose_name = "Cadastro Reservatório"
        verbose_name_plural = "Cadastro Reservatório"

    def __str__(self):
        return f'Reservatório: {self.reservatorio_cadastrado}'


class Reservatorio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    reservatorio = models.ForeignKey(Cadastro_Reservatorio, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    cloro = models.FloatField()
    ph = models.FloatField()
    fluor = models.FloatField()
    turbidez = models.FloatField()
    relatorio = models.TextField()

    def __str__(self):
        data_formatada = self.data.strftime("%d/%m/%Y")
        nome_usuario = self.usuario.username
        return f'Operador: {nome_usuario} - Reservatório: {self.reservatorio.reservatorio_cadastrado}'

        class Meta:
            verbose_name = "Reservatório"
            verbose_name_plural = "Reservatório"


class Anotacoes(models.Model):
    titulo = models.CharField(max_length=100)
    nota = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Anotações"
        verbose_name_plural = "Anotações"


class Organiza_tarefa(models.Model):
    data_agora = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_selecionada = models.DateTimeField()
    lembrete = models.TextField()
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lembrete} || para o dia {self.data_selecionada.strftime("%d/%m/%Y")}'


