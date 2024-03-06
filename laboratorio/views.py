import cmath
import datetime
import io
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4

from laboratorio.models import Numero_Media, Controle_Operacional, Cadastro_Reservatorio, Reservatorio, Anotacoes, \
    Organiza_tarefa, Informacoes_Analises_Basicas_Interna, Banco_Reservatorio_temporal
from plataforma.models import Analise_Agua_tratada, Cal_Quantidade, Tabela_estoque_cal
from django.utils import timezone
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas


# esta função aplica se para calcular a diferença de cal em horas
# podendo utilizar em qualquer monento do sistema
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


# esta função é a principal (mãe) do app laboratorio
# por ela sai as ramificalçoes para outra áreas
@login_required(login_url='operadores')
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

        # back end para veridicar se tem alguma tarefa pra hoje
        datas_selecionadas = list(Organiza_tarefa.objects.values_list('data_selecionada__date', flat=True).distinct())
        data_atual = timezone.localdate()  # data de agora
        mensagem_lembrete = ''
        for item in datas_selecionadas:
            if data_atual == item:
                print(f"A data de hoje {data_atual} coincide com uma das datas das tarefas.")
                mensagem_lembrete = 'Tem tarefas programdas para hoje, CLICK AQUI'

        # é preciso adicionar pela primera vez no ADM
        # um número para a média va em:
        # DJANGO-ADM: App Laboratorio
        # campo: Numero_medias insira manualmete 1 número
        # pode ser qualquer número como por exeplo o nímero 3
        # isso sera somente a primera vez que rodar o sistema

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
            'mensagem_lembrete': mensagem_lembrete,

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


# analises internas, podendo ter várias ramificações
# para vários tipos de analises, seria a sub-mãe deste área
@login_required(login_url='operadores')
def analises_basica_interna(request):
    if request.method == 'GET':
        informativo = Informacoes_Analises_Basicas_Interna.objects.all()
        return render(request, 'analises_basica_interna.html', {'informativo': informativo}, )

    if request.method == 'POST':
        return render(request, 'analises_basica_interna.html')


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por gravar análises feitas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
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


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por gravar análises do reservatorio feitas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
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


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por fazer calculos feitas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
def calculadora(request):
    if request.method == 'GET':
        return render(request, 'calculadora.html')
    elif request.method == 'POST':
        a = request.POST.get('a')
        b = request.POST.get('b')
        c = request.POST.get('c')

        if a is None or b is None or c is None:
            mensagem_erro = 'É necessário fornecer valores para a, b e c.'
            return render(request, 'calculadora.html', {'mensagem_erro': mensagem_erro})

        try:
            a = float(a)
            b = float(b)
            c = float(c)

            discriminante = (b ** 2) - (4 * a * c)

            raiz1 = (-b + cmath.sqrt(discriminante)) / (2 * a)
            raiz2 = (-b - cmath.sqrt(discriminante)) / (2 * a)

            return render(request, 'calculadora.html', {'raiz1': raiz1, 'raiz2': raiz2})

        except ZeroDivisionError:
            divisao_zero = 'Divisão por zero'
            return render(request, 'calculadora.html', {'divisao_zero': divisao_zero})

        except ValueError:
            mensagem_erro = 'Entrada inválida. Certifique-se de inserir valores numéricos para a, b e c.'
            return render(request, 'calculadora.html', {'mensagem_erro': mensagem_erro})


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por gravar as anotaçoes feitas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
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


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por 'ver' anotações feitas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
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


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna'
# ela é responsavel por gravar futuras tarefas pelos operadoes ou técnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
def organizador_tarefas(request):
    if request.method == 'GET':
        return render(request, 'organizador_tarefas.html')
    elif request.method == 'POST':
        nome = request.user

        data_selecionada = request.POST.get('data_selecionada')
        lembrete = request.POST.get('lembrete')

        if not all([data_selecionada, lembrete]):
            messages.error(request, 'Preencha todas as informações corretamente')
            return render(request, 'organizador_tarefas.html')

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
            messages.add_message(request, constants.SUCCESS, 'Lembrete salvo com sucesso')

        except ValueError as e:
            # Se houver um erro ao converter a data
            print("Erro ao converter a data:", e)
            messages.warning(request, f'Provável erro no sistema, tente outra vez! {e} / converter data')

        except Exception as e:
            # Captura qualquer outro tipo de exceção durante o salvamento
            print("Ocorreu um erro ao salvar o lembrete:", e)
            messages.warning(request, f'Provável erro no sistema, tente outra vez! {e} / PRESS F5')

    return render(request, 'organizador_tarefas.html')


# esta função esta ligada ou seja é filha da função 'def analises_basica_interna' ou 'def organizador_tarefas'
# existem dois caminhos para essa view, a primeira é através do html: organizador_tarefas.html a sengunda forma
# é quando existe uma tarefa para realizar no dia que aparecerá na aba laboratorio.html um borão ou link
# para ser clicado e ai sim ler e marcar como tarefa feita, ou não caso não tenha feio ainda
# ela é responsavel por pesquisar e se preciso resolvar as tarefas abertas pelos operadoes ou tecnicos que tem
# a autorização de adrentar na aba 'Laboratório'
@login_required(login_url='operadores')
def tarefas_aberta(request):
    lembretes_pendentes = Organiza_tarefa.objects.filter(concluido=False)

    if request.method == 'GET':
        # Se a solicitação for GET, a variável lembretes_pendentes é atualizada com as tarefas abertas
        lembretes_pendentes = Organiza_tarefa.objects.filter(concluido=False)

    elif request.method == 'POST':
        if 'pro_titulo' in request.POST:
            pass

        elif 'delete_tarefa' in request.POST:
            tarefa_id = request.POST.get('id_lembrete')  # Obtém o ID da tarefa enviado pelo formulário

            # Obtém o objeto Organiza_tarefa correspondente ao ID recebido
            tarefa = get_object_or_404(Organiza_tarefa, pk=tarefa_id)

            # Remove a tarefa
            tarefa.delete()

            # Atualiza a lista de tarefas abertas
            lembretes_pendentes = Organiza_tarefa.objects.filter(concluido=False)

    return render(request, 'tarefas_aberto.html', {'lembretes_pendentes': lembretes_pendentes})


@login_required(login_url='operadores')
def residencias(request):
    if request.method == 'GET':
        return render(request, 'residencias.html')
    if request.method == 'POST':
        nome = request.user
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        nome_residencia = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        cloro = request.POST.get('cloro')
        fluor = request.POST.get('fluor')
        ph = request.POST.get('ph')
        turbidez = request.POST.get('turbidez')
        coliformes = request.POST.get('analise')
        print(coliformes)

        # criar 2 tabelas
        # 1º para guardar os dados temporários
        # >> essa tabela guardará os dados ate que seja confirmada as análises
        # 2º para guarda em defenitivo sendo possivel apenas no django-admin o crud
        # >> so guardará os dados depois que forfirmar as analises

        # Verifica se os campos do formulário foram preenchidos
        if not all([cidade, bairro, rua, nome, ]):
            messages.error(request, 'Cidade, Bairro, Rua e Nome; OBRIGATÓRIO PREENCHER')
            return render(request, 'residencias.html')

        if email == '':
            email = 'Nada consta'
        if telefone == '':
            telefone = 'Nada consta'

        try:
            salva_dados_residencia = Banco_Reservatorio_temporal(
                data_agora=timezone.now(),
                usuario=nome,
                cidade=cidade,
                bairro=bairro,
                rua=rua,
                nome=nome_residencia,
                email=email,
                telefone=telefone,
                cloro=cloro,
                fluor=fluor,
                ph=ph,
                turbidez=turbidez,
                analise=coliformes,
                observacao='Nada consta'
            )
            salva_dados_residencia.save()
            messages.success(request, 'Dado salvo corretamente')

        except:
            messages.warning(request, 'Erro interno do sistema. Tente novamente.')
            messages.warning(request, 'Certifique-se de estar usando ponto em vez de vírgula, ex: "7.23" está correto')
            return render(request, 'residencias.html')

        return render(request, 'residencias.html')


@login_required(login_url='operadores')
def relatorios(request):
    if request.method == 'GET':
        nota = ''
        try:
            mosta_analise = Banco_Reservatorio_temporal.objects.order_by('-id')
        except:
            nota = 'Não foi possivel caregar nem uma irformaçao, erro interno tente outra vez!'
        if len(mosta_analise) <= 0:
            nota = 'Não existe análises em aberto'

        return render(request, 'relatorio_analises_externas.html', {'mosta_analise': mosta_analise,
                                                                    'nota': nota, })

    elif request.method == 'POST':
        nome_relatorio_pesquisa = request.POST.get('nome_pesquisa').strip()
        mensagem_pesquisa = ''
        try:
            busca_titulo = Banco_Reservatorio_temporal.objects.filter(nome__contains=nome_relatorio_pesquisa).order_by(
                '-id')
        except:
            mensagem_pesquisa = 'PRESS F5, e tente outra vez!'
        if not busca_titulo:
            mensagem_pesquisa = 'Sem resultado para a sua busca'
        return render(request, 'relatorio_analises_externas.html', {'busca_titulo': busca_titulo,
                                                                    'mensagem_pesquisa': mensagem_pesquisa,
                                                                    })


@login_required(login_url='operadores')
def pdf_relatorio(request, pk):
    if request.method == 'GET':

        # Obtendo o objeto Banco_Reservatorio_temporal com o ID fornecido (pk)
        dados_id_pk = Banco_Reservatorio_temporal.objects.get(pk=pk)

        # Atribuindo cada atributo a uma variável
        cidade = dados_id_pk.cidade
        bairro = dados_id_pk.bairro
        rua = dados_id_pk.rua
        nome = dados_id_pk.nome
        email = dados_id_pk.email
        telefone = dados_id_pk.telefone
        cloro = dados_id_pk.cloro
        fluor = dados_id_pk.fluor
        ph = dados_id_pk.ph
        turbidez = dados_id_pk.turbidez
        coliformes = dados_id_pk.analise
        data_abertura_analise = dados_id_pk.data_agora
        operador = dados_id_pk.usuario
        observacao = dados_id_pk.observacao
        id_pdf = dados_id_pk.id

        # Criar PDF
        buffer = io.BytesIO()
        cnv = canvas.Canvas(buffer)
        cnv.setFont("Helvetica", 22)
        cnv.drawString(25, 790, "SERVIÇO AUTÔNOMO DE ÁGUA E ESGOTO DE IPUÃ")
        cnv.setFont("Helvetica", 15)
        cnv.drawString(47, 765, "Este documento só será válido com a assinatura do químico responsável")
        cnv.line(10, 780, 580, 780)
        cnv.setFont("Helvetica", 22)
        cnv.drawString(47, 725, "Resultado das Análises da água consumida:")

        cnv.setFont("Helvetica", 15)
        cnv.drawString(47, 695, f"Autor das análises: {operador}")
        cnv.drawString(47, 675, f"Data das análises: {dados_id_pk.data_agora.strftime('%d/%m/%Y')}")

        cnv.drawString(47, 645, f"Cidade: {cidade}")
        cnv.drawString(47, 625, f"Bairro: {bairro}")
        cnv.drawString(47, 605, f"Rua/av.: {rua}")
        cnv.drawString(47, 585, f"Nome: {nome}")

        cnv.setFont("Helvetica", 18)
        cnv.drawString(47, 530, f"CLORO: {cloro}")
        cnv.drawString(300, 530, f"pH: {ph}")
        cnv.drawString(47, 480, f"FLÚOR: {fluor}")
        cnv.drawString(300, 480, f"TURBIDEZ: {turbidez}")
        cnv.drawString(47, 430, f"COLIFORMES: {coliformes}")

        cnv.setFont("Helvetica", 14)
        tamanho = len(observacao)
        cnv.drawString(47, 370, f"OBSERVAÇÕES:")

        # Divide o texto em linhas
        # A variavel observacao sempre que for maior que a folha A4
        # o código a seguir conta as strings e quebra as linha.
        linhas = [observacao[i:i + 70] for i in range(0, tamanho, 70)]

        # Escreve as linhas no PDF
        y = 340  # Posição Y inicial
        for linha in linhas:
            cnv.drawString(70, y, f"{linha}")
            y -= 15  # Move para a próxima linha

        cnv.setFont("Helvetica", 12)
        cnv.drawString(27, 80, f"Assinatura do químico responsável: __________________________________________________")

        cnv.save()

        # Retornar o PDF como uma resposta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="pdf_{id_pdf}_analise.pdf"'
        response.write(buffer.getvalue())

        return response

    elif request.method == 'POST':
        return render(request, 'id_pdf.html')


@login_required(login_url='operadores')
def index_relatorio(request):
    if request.method == 'GET':
        return render(request, 'index_relatorio.html')
    elif request.method == 'POST':
        return render(request, 'index_relatorio.html')


@login_required(login_url='operadores')
def patrimonio_cadastrado(request):
    if request.method == 'GET':

        return render(request, 'patrimonio_cadastrado.html')
    elif request.method == 'POST':
        return render(request, 'patrimonio_cadastrado.html')


@login_required(login_url='operadores')
def monitoramento_diario(request):
    if request.method == 'GET':
        pdf_analise_agua_limpa = Analise_Agua_tratada.objects.all()

        # Criando um dicionário para armazenar as análises agrupadas por data completa
        pdf_analise_agua_por_data = defaultdict(list)
        for analise in pdf_analise_agua_limpa:
            data_completa = analise.data_analise_agua.date()
            pdf_analise_agua_por_data[data_completa].append(analise)

        cont = len(pdf_analise_agua_limpa)

        return render(request, 'relatorio_monitoramento_diario.html',
                      {'pdf_analise_agua_por_data': dict(pdf_analise_agua_por_data), 'cont': cont})
    elif request.method == 'POST':

        data_do_formulario = request.POST.get('data')

        # Recupera os IDs das análises do formulário como uma string
        analise_ids_str = request.POST.get('analise_ids')

        # Converte a string de IDs em uma lista de inteiros
        analise_ids = [int(id) for id in analise_ids_str.split(',') if id]

        ids_lista = []

        for id_analise in analise_ids:
            analise = Analise_Agua_tratada.objects.get(pk=id_analise)

            # Adiciona o objeto à lista em vez de apenas o ID
            ids_lista.append(analise)

        # Criar PDF
        buffer = io.BytesIO()
        cnv = canvas.Canvas(buffer)

        # Definir o tamanho da fonte
        tamanho_fonte = 40  # Tamanho da fonte desejado
        cnv.setFontSize(tamanho_fonte)
        cnv.drawString(90, 787, "Monitoramento Diário")
        tamanho_fonte = 16  # Tamanho da fonte desejado
        cnv.setFontSize(tamanho_fonte)
        cnv.drawString(10, 755, "Saae Ipuã-SP")  # buscar cidade no banco
        tamanho_fonte = 20  # Tamanho da fonte desejado
        cnv.setFontSize(tamanho_fonte)
        cnv.drawString(10, 730, f"{data_do_formulario}")
        cnv.drawString(6, 730, f"____________________________________________________")
        a = 20  # nome do operador
        b = 700  # nome do operador
        c = 290  # cloro
        d = 700  # cloro
        e = 365  # fluor
        f = 700  # fluor
        g = 440  # ph
        h = 700  # ph
        i = 500  # turbidez
        j = 700  # turbidez
        k = 200  # horario
        l = 700  # horario
        tamanho_fonte = 12  # Tamanho da fonte desejado
        cnv.setFontSize(tamanho_fonte)
        for analise in ids_lista:
            hora = analise.data_analise_agua.strftime("%H:%M")
            cnv.drawString(a, b, f"Operador: {analise.usuario}")
            cnv.drawString(k, l, f"horario: {hora}")
            cnv.drawString(c, d, f"Cloro: {analise.cloro}")
            cnv.drawString(e, f, f"Flúor: {analise.fluor}")
            cnv.drawString(g, h, f"pH: {analise.ph}")
            cnv.drawString(i, j, f"Turbidez: {analise.turbidez}")

            # Atualizar as coordenadas para a próxima iteração
            b -= 22  # Por exemplo, diminuir a coordenada y para mover para baixo na página
            d -= 22  # Outra opção para mover para baixo o texto "Cloro"
            f -= 22
            h -= 22
            j -= 22
            l -= 22
        cnv.save()

        # Retornar o PDF como uma resposta HTTP

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="PDF_monitoramento_diario.pdf"'
        response.write(buffer.getvalue())

    return response


# sair do sistema
def logout_view(request):
    logout(request)
    # Redirecione para onde você deseja após o logout
    return redirect('operadores')
