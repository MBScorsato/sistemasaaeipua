from django.contrib import admin
from django.utils.timezone import activate
from .models import Analise_Agua_tratada, Analise_Agua_bruta, Parametro, Hidrometro, SaidaCaminhaPipa, Mensagem, Laboratorio

class Analise_Agua_tratadaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cloro', 'ph', 'fluor', 'cor', 'turbidez', 'data_analise_agua', 'relatorio')

    def changelist_view(self, request, extra_context=None):
        activate('America/Sao_Paulo')
        return super().changelist_view(request, extra_context=extra_context)


class Analise_Agua_brutadaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'decantada_cor', 'decantada_ph', 'decantada_turbidez',
                    'bruta_cor', 'bruta_ph', 'bruta_turbidez',
                    'relatorio',
                    'qeta', 'qcal', 'qpac')

    def changelist_view(self, request, extra_context=None):
        activate('America/Sao_Paulo')
        return super().changelist_view(request, extra_context=extra_context)


# Registre o modelo e o admin
admin.site.register(Analise_Agua_tratada, Analise_Agua_tratadaAdmin)
admin.site.register(Analise_Agua_bruta, Analise_Agua_brutadaAdmin)
admin.site.register(Parametro)
# admin.site.register(Cal_Quantidade, Cal_QuantidadeAdmin)
# admin.site.register(Estoque_Cal, Estoque_CalAdmin)
# admin.site.register(Tabela_estoque_cal)
admin.site.register(Hidrometro)
admin.site.register(SaidaCaminhaPipa)
admin.site.register(Mensagem)
admin.site.register(Laboratorio)
