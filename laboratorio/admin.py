from django.contrib import admin

from laboratorio.models import Numero_Media, Controle_Operacional, Cadastro_Reservatorio, Reservatorio, \
    Anotacoes, Organiza_tarefa, Informacoes_Analises_Basicas_Interna, Banco_Reservatorio_temporal, \
    Registro_manutencao_externa, Registro_patrimonio

admin.site.register(Numero_Media)
admin.site.register(Controle_Operacional)
admin.site.register(Cadastro_Reservatorio)
admin.site.register(Reservatorio)
admin.site.register(Anotacoes)
admin.site.register(Organiza_tarefa)
admin.site.register(Informacoes_Analises_Basicas_Interna)
admin.site.register(Banco_Reservatorio_temporal)
admin.site.register(Registro_manutencao_externa)

class RegistroPatrimonioAdmin(admin.ModelAdmin):
    list_display = ('id', 'objeto', 'funcao_do_objeto', 'local_de_uso', 'em_uso', 'data')

admin.site.register(Registro_patrimonio, RegistroPatrimonioAdmin)
