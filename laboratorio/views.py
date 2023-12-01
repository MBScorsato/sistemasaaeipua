import cmath
import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from laboratorio.models import Numero_Media, Controle_Operacional, Cadastro_Reservatorio, Reservatorio, Anotacoes, \
    Organiza_tarefa
from plataforma.models import Analise_Agua_tratada, Cal_Quantidade, Tabela_estoque_cal
from django.utils import timezone
from django.shortcuts import render


def calcular_diferenca_em_horas():
    # Consulta para obter as datas (horas)
    cal = Cal_Quantidade.objects.order_by('-id')[:2].values_list('data', flat=True)
    dates = list(cal)

    if len(dates) >= 2:
        data1 = dates[0]
        data2 = dates[1]
        diferenca = data1 - data2
        resultado = int(diferenca.total_seconds() / 3600)   # Converte os segundos em horas
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

        ultimas_analises_fluor = Analise_Agua_tratada.objects.order_by('-id')[:valor_n].values_list('fluor', flat=True)
        valores_fluor = list(ultimas_analises_fluor)
        if valores_fluor:
            media_fluor = sum(valores_fluor) / len(valores_fluor)
        else:
            media_fluor = 0.00

        # buscar quantidades de sacos de cal no estoque
        quantidade_cal_estoque = Tabela_estoque_cal.objects.first().resultado_final
        r_cal = quantidade_cal_estoque // 20

        print("Sacos de cal no estoque:", r_cal)

        # Análises para os gráficos daqui para baixo
        #
        #

        # cloro
        grafico_cloro = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('cloro', flat=True)
        datas = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('data_analise_agua', flat=True)
        # Convertendo para o fuso horário desejado (substitua 'fuso_horario_desejado' pelo seu fuso horário)
        datas_no_fuso_horario = [data.astimezone(timezone.get_current_timezone()) for data in datas]
        horas_cloro = [data.strftime('%H:%M') for data in datas_no_fuso_horario]

        # horas cloro
        horasC1 = horas_cloro[0]
        horasC2 = horas_cloro[1]
        horasC3 = horas_cloro[2]

        # valor cloro
        valor_g1_cloro = grafico_cloro[0]
        valor_g2_cloro = grafico_cloro[1]
        valor_g3_cloro = grafico_cloro[2]

        # ph
        grafico_ph = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('ph', flat=True)
        datas = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('data_analise_agua', flat=True)
        # Convertendo para o fuso horário desejado (substitua 'fuso_horario_desejado' pelo seu fuso horário)
        datas_no_fuso_horario = [data.astimezone(timezone.get_current_timezone()) for data in datas]
        horas = [data.strftime('%H:%M') for data in datas_no_fuso_horario]

        # horas pH
        horasP1 = horas[0]
        horasP2 = horas[1]
        horasP3 = horas[2]

        # valor ph
        valor_g1_ph = grafico_ph[0]
        valor_g2_ph = grafico_ph[1]
        valor_g3_ph = grafico_ph[2]

        # flúor
        grafico_fluor = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('fluor', flat=True)
        datas = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('data_analise_agua', flat=True)
        # Convertendo para o fuso horário desejado (substitua 'fuso_horario_desejado' pelo seu fuso horário)
        datas_no_fuso_horario = [data.astimezone(timezone.get_current_timezone()) for data in datas]
        horas = [data.strftime('%H:%M') for data in datas_no_fuso_horario]

        # horas flúor
        horasF1 = horas[0]
        horasF2 = horas[1]
        horasF3 = horas[2]

        # valor flúor
        valor_g1_fluor = grafico_fluor[0]
        valor_g2_fluor = grafico_fluor[1]
        valor_g3_fluor = grafico_fluor[2]

        # turbidez
        grafico_turbidez = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('turbidez', flat=True)

        datas = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('data_analise_agua', flat=True)
        # Convertendo para o fuso horário desejado (substitua 'fuso_horario_desejado' pelo seu fuso horário)
        datas_no_fuso_horario = [data.astimezone(timezone.get_current_timezone()) for data in datas]
        horas_turbudez = [data.strftime('%H:%M') for data in datas_no_fuso_horario]

        # horas turbidez
        horasT1 = horas_turbudez[0]
        horasT2 = horas_turbudez[1]
        horasT3 = horas_turbudez[2]

        # valor turbidez
        valor_g1_turbidez = grafico_turbidez[0]
        valor_g2_turbidez = grafico_turbidez[1]
        valor_g3_turbidez = grafico_turbidez[2]

        # cor
        grafico_cor = Analise_Agua_tratada.objects.order_by('-id')[:3].values_list('cor', flat=True)

        # Convertendo para o fuso horário desejado (substitua 'fuso_horario_desejado' pelo seu fuso horário)
        datas_no_fuso_horario = [data.astimezone(timezone.get_current_timezone()) for data in datas]
        horas_cor = [data.strftime('%H:%M') for data in datas_no_fuso_horario]

        # horas cor
        horasCOR1 = horas_cor[0]
        horasCOR2 = horas_cor[1]
        horasCOR3 = horas_cor[2]

        valor_g1_cor = grafico_cor[0]
        valor_g2_cor = grafico_cor[1]
        valor_g3_cor = grafico_cor[2]

        # aviso caso tenha alguma tarefa




        return render(request, 'laboratorio.html', {
                                                    'media_cloro': media_cloro,
                                                    'media_turbidez': media_turbidez,
                                                    'media_ph': media_ph,
                                                    'media_fluor': media_fluor,
                                                    'resultado': resultado,
                                                    'r_cal': r_cal,
                                                    'valor_g1_cloro': valor_g1_cloro,  # valor cloro
                                                    'valor_g2_cloro': valor_g2_cloro,
                                                    'valor_g3_cloro': valor_g3_cloro,
                                                    'valor_g1_ph': valor_g1_ph,  # valor pH
                                                    'valor_g2_ph': valor_g2_ph,
                                                    'valor_g3_ph': valor_g3_ph,
                                                    'valor_g1_fluor': valor_g1_fluor,  # valor flúor
                                                    'valor_g2_fluor': valor_g2_fluor,
                                                    'valor_g3_fluor': valor_g3_fluor,
                                                    'valor_g1_turbidez': valor_g1_turbidez,  # valor turbdez
                                                    'valor_g2_turbidez': valor_g2_turbidez,
                                                    'valor_g3_turbidez': valor_g3_turbidez,
                                                    'valor_g1_cor': valor_g1_cor,  # valor cor
                                                    'valor_g2_cor': valor_g2_cor,
                                                    'valor_g3_cor': valor_g3_cor,
                                                    'horasC1': horasC1,  # horas cloro
                                                    'horasC2': horasC2,
                                                    'horasC3': horasC3,
                                                    'horasP1': horasP1,  # horas ph
                                                    'horasP2': horasP2,
                                                    'horasP3': horasP3,
                                                    'horasF1': horasF1,  # horas flúor
                                                    'horasF2': horasF2,
                                                    'horasF3': horasF3,
                                                    'horasT1': horasT1,  # horas turbidez
                                                    'horasT2': horasT2,
                                                    'horasT3': horasT3,
                                                    'horasCOR1': horasCOR1,  # horas cor
                                                    'horasCOR2': horasCOR2,
                                                    'horasCOR3': horasCOR3,

                                                    })
    elif request.method == 'POST':

        # quantidade de analises para calculo de média
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

            # apague o registro
            ultimo_registro.delete()

            # e salve um novo, ao estilo CRUD
            salvar_n.save()
        except Exception as e:
            pass

        # forçar um F5 na página
        resultado = calcular_diferenca_em_horas()
        response = HttpResponse(render(request, 'laboratorio.html', {'resultado': resultado}))
        response['refresh'] = '1;url=' + request.META.get('HTTP_REFERER', '/')
        return response


def analises_basica_interna(request):
    if request.method == 'GET':
        return render(request, 'analises_basica_interna.html')

    if request.method == 'POST':
        return render(request, 'analises_basica_interna.html')


def controle_operacional(request):
    if request.method == 'GET':
        return render(request, 'controle_operacional.html')

    if request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user

        pre_cloro = request.POST.get('pre_cloro')
        cloro_estacao = request.POST.get('cloro_estacao')
        turbidez_estacao = request.POST.get('turbidez_estacao')
        relatorio = request.POST.get('relatorio')
        fluor = request.POST.get('fluor')

        if relatorio == '':
            relatorio = 'Nada consta'

        # Verifica se todos os campos do formulário foram preenchidos
        if not all([pre_cloro, cloro_estacao, turbidez_estacao, fluor]):
            messages.error(request, 'Preencha todas as informações corretamente')
            return render(request, 'controle_operacional.html')

        try:
            salvar_dados = Controle_Operacional(usuario=nome,
                                                data=datetime.datetime.now(),
                                                pre_cloro=pre_cloro,
                                                cloro_esstacao=cloro_estacao,
                                                fluor=fluor,
                                                turbidez_estacao=turbidez_estacao,
                                                relatorio=relatorio,

                                                )
            salvar_dados.save()
            messages.add_message(request, constants.SUCCESS, 'Dados salvo com sucesso')

        except Exception as e:

            print("Erro ao salvar:", e)  # Isso imprimirá informações sobre o erro no console do servidor
            messages.warning(request, 'Provável erro no sistema, tente outra vez!')
            messages.warning(request, 'Certifique-se de estar usando ponto em vez de vírgula, ex: "7.23" está '
                                      'correto')

        return render(request, 'controle_operacional.html')


def reservatorio(request):
    if request.method == 'GET':
        reservatorios = Cadastro_Reservatorio.objects.all()
        return render(request, 'reservatorio.html', {'reservatorios': reservatorios})

    elif request.method == 'POST':
        nome = request.user
        reservatorios = Cadastro_Reservatorio.objects.all()

        id_reservatorios = request.POST.getlist('reservatorios')

        # Obtém objetos Cadastro_Reservatorio correspondentes aos IDs
        reservatorios_selecionados = Cadastro_Reservatorio.objects.filter(pk__in=id_reservatorios)

        cloro = request.POST.get('cloro_reservatorio')
        ph = request.POST.get('ph_reservatorio')
        fluor = request.POST.get('fluor_reservatorio')
        turbidez = request.POST.get('turbidez_reservatorio')
        relatorio = request.POST.get('relatorio')

        if relatorio == '':
            relatorio = 'Nada consta'

        # Verifica se todos os campos do formulário foram preenchidos
        if not all([cloro, ph, turbidez, fluor, id_reservatorios]):
            messages.error(request, 'Preencha todas as informações corretamente')
            return render(request, 'controle_operacional.html')

        try:
            for reservatorio_selecionado in reservatorios_selecionados:
                # Cria um objeto Reservatorio para cada reservatório selecionado
                dados_reservatorio = Reservatorio(usuario=nome,
                                                  reservatorio=reservatorio_selecionado,
                                                  data=datetime.datetime.now(),
                                                  cloro=cloro,
                                                  ph=ph,
                                                  fluor=fluor,
                                                  turbidez=turbidez,
                                                  relatorio=relatorio)
                dados_reservatorio.save()
                messages.success(request, 'Dados preenchidos corretamente')

        except Exception as e:
            print("Erro ao salvar:", e)  # Isso imprimirá informações sobre o erro no console do servidor
            messages.warning(request, 'Provável erro no sistema, tente outra vez!')
            messages.warning(request, 'Certifique-se de estar usando ponto em vez de vírgula, ex: "7.23" está '
                                      'correto')
            print("Erro ao salvar a análise:", e)

        return render(request, 'reservatorio.html', {'reservatorios_selecionados': reservatorios_selecionados,
                                                     'reservatorios': reservatorios,
                                                     })


def calculadora(request):
    if request.method == 'GET':
        return render(request, 'calculadora.html')
    elif request.method == 'POST':
        # bhaskara
        a = float(request.POST.get('a'))
        b = float(request.POST.get('b'))
        c = float(request.POST.get('c'))

        discriminante = (b ** 2) - (4 * a * c)

        # Calcula as raízes
        raiz1 = (-b + cmath.sqrt(discriminante)) / (2 * a)
        raiz2 = (-b - cmath.sqrt(discriminante)) / (2 * a)

        return render(request, 'calculadora.html', {'raiz1': raiz1,
                                                    'raiz2': raiz2})


def anotacoes_gerais(request):

    if request.method == 'GET':
        return render(request, 'anotacoes_gerais.html')
    elif request.method == 'POST':
        nome = request.user

        titulo = request.POST.get('titulo')
        nota = request.POST.get('nota')

        # Verifica se todos os campos do formulário foram preenchidos
        if not all([nota, titulo]):
            messages.error(request, 'Preencha todas as informações corretamente')
            return render(request, 'anotacoes_gerais.html')

        try:
            salvar_nota_titulo = Anotacoes(titulo=titulo,
                                           nota=nota,
                                           data=datetime.datetime.now(),
                                           usuario=nome
                                           )
            salvar_nota_titulo.save()
            messages.success(request, 'Sua nota foi salva com sucesso!')

        except Exception as e:
            print("Erro ao salvar:", e)  # Isso imprimirá informações sobre o erro no console do servidor
            messages.warning(request, 'Provável erro no sistema, tente outra vez!')

        return render(request, 'anotacoes_gerais.html')


def ver_anotacoes(request):
    if request.method == 'GET':
        notas = Anotacoes.objects.all().order_by('-id')
        return render(request, 'ver_anotacoes.html', {'notas': notas,

                                                      })
    elif request.method == 'POST':
        pro_titulo = request.POST.get('pro_titulo')
        sem_resultado = None  # Definir um valor padrão

        if pro_titulo == '':
            notas = Anotacoes.objects.all().order_by('-id')
            return render(request, 'ver_anotacoes.html', {'notas': notas})

        busca_titulo = Anotacoes.objects.filter(titulo__contains=pro_titulo).order_by('-id')

        if len(busca_titulo) <= 0:
            sem_resultado = 'Sua busca teve 0 resultado'

        return render(request, 'ver_anotacoes.html', {'busca_titulo': busca_titulo,
                                                      'sem_resultado': sem_resultado})


def organizador_tarefas(request):
    if request.method == 'GET':
        return render(request, 'organizador_tarefas.html')
    elif request.method == 'POST':
        nome = request.user

        data_selecionada = request.POST.get('data_selecionada')
        lembrete = request.POST.get('lembrete')
        print(data_selecionada)
        print(lembrete)

        try:
            # Convertendo a string da data para um objeto datetime
            data_formatada = datetime.datetime.strptime(data_selecionada, '%Y-%m-%d').date()

            salvar_lembrete = Organiza_tarefa(
                data_agora=timezone.now(),
                usuario=nome,
                data_selecionada=data_formatada,
                lembrete=lembrete,
                # O campo 'concluido' por definição já recebe False (model.py)
            )
            salvar_lembrete.save()

        except ValueError as e:
            # Se houver um erro ao converter a data
            print("Erro ao converter a data:", e)

        except Exception as e:
            # Captura qualquer outro tipo de exceção durante o salvamento
            print("Ocorreu um erro ao salvar o lembrete:", e)
            # Aqui você pode adicionar ações adicionais, como logs ou mensagens para o usuário

    return render(request, 'organizador_tarefas.html')


def tarefas_aberta(request):
    if request.method == 'GET':
        return render(request, 'tarefas_aberto.html')
    elif request.method == 'POST':
        return render(request, 'tarefas_aberto.html')