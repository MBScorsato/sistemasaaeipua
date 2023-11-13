from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render

from laboratorio.models import Numero_Media
from plataforma.models import Laboratorio, Parametro, Analise_Agua_tratada, Cal_Quantidade, Estoque_Cal, \
    Tabela_estoque_cal


def calcular_diferenca_em_horas():
    # Consulta para obter as datas (horas)
    cal = Cal_Quantidade.objects.order_by('-id')[:2].values_list('data', flat=True)
    dates = list(cal)

    if len(dates) >= 2:
        data1 = dates[0]
        data2 = dates[1]
        diferenca = data1 - data2
        resultado = int(diferenca.total_seconds() / 3600)  # Converte os segundos em horas
        print("Diferença em horas:", resultado)
        return resultado
    else:
        print("Não há datas suficientes para calcular a diferença em horas")
        return 0


def laboratorio(request):
    if request.method == 'GET':
        usuario = request.user
        if hasattr(usuario, 'laboratorio'):
            laboratorio = usuario.laboratorio
            esta_autorizado = laboratorio.autorizado
            if not esta_autorizado:
                return HttpResponse('<h1>Você tentou acessar de forma não permitida, hahahaha, tente outra vez!</h1>')
        else:
            return HttpResponse('<h1>Você não tem permissão para acessar esta página.</h1>')

        valor_n = Numero_Media.objects.first().n
        if valor_n < 0:
            valor_n = 0
        print("Valor salvo no banco para média:", valor_n)

        resultado = calcular_diferenca_em_horas()

        ultimas_analises_cloro = Analise_Agua_tratada.objects.order_by('-id')[:valor_n].values_list('cloro', flat=True)
        valores_cloro = list(ultimas_analises_cloro)
        if valores_cloro:
            media_cloro = sum(valores_cloro) / len(valores_cloro)
        else:
            media_cloro = 0.00

        ultimas_analises_turbidez = Analise_Agua_tratada.objects.order_by('-id')[:valor_n].values_list('turbidez',
                                                                                                       flat=True)
        valores_turbidez = list(ultimas_analises_turbidez)
        if valores_turbidez:
            media_turbidez = sum(valores_turbidez) / len(valores_turbidez)
        else:
            media_turbidez = 0.00

        ultimas_analises_ph = Analise_Agua_tratada.objects.order_by('-id')[:valor_n].values_list('ph', flat=True)
        valores_ph = list(ultimas_analises_ph)
        if valores_ph:
            media_ph = sum(valores_ph) / len(valores_ph)
        else:
            media_ph = 0.00

        media_fluor = valor_n

        # buscar quantidades de sacos de cal no estoque
        quantidade_cal_estoque = Tabela_estoque_cal.objects.first().resultado_final
        r_cal = quantidade_cal_estoque // 20

        print("Sacos de cal no estoque:", r_cal)

        return render(request, 'laboratorio.html', {'media_cloro': media_cloro,
                                                    'media_turbidez': media_turbidez,
                                                    'media_ph': media_ph,
                                                    'media_fluor': media_fluor,
                                                    'resultado': resultado,
                                                    'r_cal': r_cal,

                                                    })
    elif request.method == 'POST':
        ultimo_registro = Numero_Media.objects.all()
        if not ultimo_registro:
            len(ultimo_registro) <= 0
            ultimo_registro = 12
            print(ultimo_registro)
            salvar_n_1 = Numero_Media(n=12)
            salvar_n_1.save()

        n = request.POST.get('numero_analises')

        try:
            salvar_n = Numero_Media(n=n)
            ultimo_registro = Numero_Media.objects.latest('n')
            ultimo_registro.delete()

            salvar_n.save()
        except Exception as e:
            pass
        resultado = calcular_diferenca_em_horas()
        response = HttpResponse(render(request, 'laboratorio.html', {'resultado': resultado}))
        response['refresh'] = '1;url=' + request.META.get('HTTP_REFERER', '/')
        return response
