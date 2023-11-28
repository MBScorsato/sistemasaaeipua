from django.db.models.signals import pre_save, post_save
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User


class Analise_Agua_tratada(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Campo para relacionar com o usuário
    cloro = models.FloatField()
    ph = models.FloatField()
    fluor = models.FloatField()
    cor = models.FloatField()
    turbidez = models.FloatField()
    relatorio = models.TextField()
    data_analise_agua = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Formatando a data no padrão "dia/mês/ano horas:minutos"
        data_hora_formatada = self.data_analise_agua.strftime("%d/%m/%Y %H:%M")

        # Obtendo o nome de usuário do usuário relacionado
        nome_usuario = self.usuario.username

        return f"{nome_usuario} - Data da análise: {data_hora_formatada}"


class Analise_Agua_bruta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Campo para relacionar com o usuário

    decantada_ph = models.FloatField()
    decantada_cor = models.FloatField()
    decantada_turbidez = models.FloatField()

    bruta_ph = models.FloatField()
    bruta_cor = models.FloatField()
    bruta_turbidez = models.FloatField()

    relatorio = models.TextField()

    qeta = models.FloatField()
    qcal = models.FloatField()
    qpac = models.FloatField()

    data_analise_agua = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Formatando a data no padrão "dia/mês/ano horas:minutos"
        data_hora_formatada = self.data_analise_agua.strftime("%d/%m/%Y %H:%M")

        # Obtendo o nome de usuário do usuário relacionado
        nome_usuario = self.usuario.username

        return f"{nome_usuario} - Data da análise: {data_hora_formatada}"


class OperadoresAviso(models.Model):
    aviso = models.TextField()

    def __str__(self):
        return self.aviso


class Parametro(models.Model):
    fluor_min = models.FloatField()
    fluor_ideal = models.FloatField()
    fluor_max = models.FloatField()
    cloro_min = models.FloatField()
    cloro_ideal = models.FloatField()
    cloro_max = models.FloatField()
    cor_min = models.FloatField()
    cor_ideal = models.FloatField()
    cor_max = models.FloatField()
    ph_min = models.FloatField()
    ph_ideal = models.FloatField()
    ph_max = models.FloatField()
    turbidez_min = models.FloatField()
    turbidez_ideal = models.FloatField()
    turbidez_max = models.FloatField()
    parametro = models.TextField()

    def __str__(self):
        return self.parametro


# essas class salva qual operador ultilizou cal
class Cal_Quantidade(models.Model):
    quantidade = models.CharField(max_length=20)
    data = models.DateTimeField(default=timezone.now)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    relatorio = models.TextField()

    def __str__(self):
        nome_usuario = self.operador.username
        return f"Operador: {nome_usuario} - 1 saco de cal"


# essa class salva o abastecimeto no estoque
class Estoque_Cal(models.Model):
    cal_quilo = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Formatando a data no padrão "dia/mês/ano horas:minutos"
        data_hora_formatada = self.data.strftime("%d/%m/%Y %H:%M")
        return f"Estoque carregado - Data/Hora: {data_hora_formatada}"


class Tabela_estoque_cal(models.Model):
    resultado_final = models.IntegerField()

    def __str__(self):
        return str(self.resultado_final)


class Estoque_Cal(models.Model):
    cal_quilo = models.IntegerField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Formatando a data no padrão "dia/mês/ano horas:minutos"
        data_hora_formatada = self.data.strftime("%d/%m/%Y %H:%M")
        return f"Estoque carregado - Data/Hora: {data_hora_formatada}"


class Tabela_estoque_cal(models.Model):
    resultado_final = models.IntegerField(default=0)

    def __str__(self):
        return str(self.resultado_final)


@receiver(post_save, sender=Estoque_Cal)
def atualizar_tabela_estoque_cal(sender, instance, created, **kwargs):
    if created:
        # Obtendo o objeto Tabela_estoque_cal
        tabela_estoque_cal = Tabela_estoque_cal.objects.first()

        # Verificando se há algum objeto Tabela_estoque_cal no banco de dados
        if tabela_estoque_cal:
            # Somando o valor cal_quilo do Estoque_Cal com o resultado_final da Tabela_estoque_cal
            tabela_estoque_cal.resultado_final += instance.cal_quilo
            tabela_estoque_cal.save()
        else:
            # Caso não haja objeto Tabela_estoque_cal no banco de dados, criamos um novo
            Tabela_estoque_cal.objects.create(resultado_final=instance.cal_quilo)


class Hidrometro(models.Model):
    data = models.DateTimeField(default=timezone.now)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    hidrometro_150 = models.FloatField()
    hidrometro_200 = models.FloatField()
    hidrometro_poco = models.FloatField()
    relatorio = models.TextField()

    def __str__(self):
        nome_usuario = self.operador.username
        return f"{nome_usuario}"


class SaidaCaminhaPipa(models.Model):
    data = models.DateTimeField(default=timezone.now)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    relatorio = models.TextField()
    placa = models.CharField(max_length=10)
    destino = models.CharField(max_length=50)
    motorista = models.CharField(max_length=60)
    quantidade = models.FloatField()

    def __str__(self):
        return f"{self.data.strftime('%d-%m-%Y')} - {self.operador.username} - Click para mais detalhes"


# salva as mensagens
class Mensagem(models.Model):
    operador = models.CharField(max_length=30)
    mensagem = models.TextField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.operador} diz: {self.mensagem}"


# esta class tem um valor booleano
# para o admin  pode dizer através
# do click na no admin
# quem vai poder entrar no link
# Laboratório.
class Laboratorio(models.Model):
    operador = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        if self.autorizado:
            return f"{self.operador} está autorizado para acessar a área de Laboratório"
        else:
            return f"{self.operador} não está autorizado para acessar a área de Laboratório"
