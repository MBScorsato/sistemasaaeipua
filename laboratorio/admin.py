from django.contrib import admin

from laboratorio.models import Numero_Media, Controle_Operacional, Cadastro_Reservatorio, Reservatorio, \
    Anotacoes, Organiza_tarefa

admin.site.register(Numero_Media)
admin.site.register(Controle_Operacional)
admin.site.register(Cadastro_Reservatorio)
admin.site.register(Reservatorio)
admin.site.register(Anotacoes)
admin.site.register(Organiza_tarefa)