from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render

from laboratorio.models import Numero_Media
from plataforma.models import Laboratorio, Parametro, Analise_Agua_tratada, Cal_Quantidade


def laboratorio(request):
    if request.method == 'GET':
        # Obtém o usuário logado
        usuario = request.user

        # Verifica se o usuário tem um relacionamento com o modelo Laboratorio
        # nunca mexer nesse bloco
        if hasattr(usuario, 'laboratorio'):
            laboratorio = usuario.laboratorio

            # Verifica o campo 'autorizado' do modelo Laboratorio
            esta_autorizado = laboratorio.autorizado

            if not esta_autorizado:
                return HttpResponse('<h1>Você tentou acessar de forma não permitida, hahahaha, tente outra vez!</h1>')
        else:
            return HttpResponse('<h1>Você não tem permissão para acessar esta página.</h1>')

        # apartir daqui tem permissão para mexer, antes disso de forma alguma mexer
        # bloco amarrado com a view da pasta plataforma e o seus html's correspondetes
        # representa a permissão ou não dos usuários
        # tambem é importe: no if not esta_autorizado, tem uma verificação para possíveis fraudes

        # segue os códigos com as médias e gráficos, antes disso não mexer de forma alguma

        media_cloro = []
        media_turbidez = []
        media_ph = []
        media_fluor = []
        cal = []

        ######
        # consulta para obter as data(horas)
        cal = Cal_Quantidade.objects.order_by('-id')[:2].values_list('data', flat=True)
        dates = list(cal)

        if len(dates) >= 2:
            data1 = dates[0]
            data2 = dates[1]
            diferenca = data1 - data2
            resultado = int(diferenca.total_seconds() / 3600)  # Converte os segundos em horas
            print("Diferença em horas:", resultado)
        else:
            print("Não há datas suficientes para calcular a diferença em horas")

        ######
        # Consulta para obter as últimas análises de cloro do modelo Analise_Agua_tratada
        ultimas_analises_cloro = Analise_Agua_tratada.objects.order_by('-id')[:6].values_list('cloro', flat=True)

        # Converte os valores de cloro em uma lista
        valores_cloro = list(ultimas_analises_cloro)

        if valores_cloro:
            media_cloro = sum(valores_cloro) / len(valores_cloro)
        else:
            media_cloro = 0.00  # Define uma média de 0 se não houver valores

        ######
        # Consulta para obter as últimas análises de turbidez do modelo Analise_Agua_tratada
        ultimas_analises_turbidez = Analise_Agua_tratada.objects.order_by('-id')[:6].values_list('turbidez', flat=True)

        # Converte os valores de cloro em uma lista
        valores_turbidez = list(ultimas_analises_turbidez)

        if valores_turbidez:
            media_turbidez = sum(valores_turbidez) / len(valores_turbidez)
        else:
            media_turbidez = 0.00  # Define uma média de 0 se não houver valores

        ######
        # Consulta para obter as últimas análises de ph do modelo Analise_Agua_tratada
        ultimas_analises_ph = Analise_Agua_tratada.objects.order_by('-id')[:6].values_list('ph', flat=True)

        # Converte os valores de cloro em uma lista
        valores_ph = list(ultimas_analises_ph)

        if valores_ph:
            media_ph = sum(valores_ph) / len(valores_ph)
        else:
            media_ph = 0.00  # Define uma média de 0 se não houver valores

        media_fluor = 0.68

        return render(request, 'laboratorio.html', {'media_cloro': media_cloro,
                                                    'media_turbidez': media_turbidez,
                                                    'media_ph': media_ph,
                                                    'media_fluor': media_fluor,
                                                    'resultado': resultado,

                                                    })
    elif request.method == 'POST':

        dado_formulario = request.POST.get('numero_analises')

        return render(request, 'laboratorio.html', {
            'dado_formulario': dado_formulario,

        })
