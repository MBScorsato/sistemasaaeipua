import datetime
import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from plataforma.models import Analise_Agua_tratada, Analise_Agua_bruta, OperadoresAviso, Parametro, Tabela_estoque_cal, \
    Cal_Quantidade, Hidrometro, SaidaCaminhaPipa, Mensagem


# Def é a principal, depois de logar cai nesta def
@login_required(login_url='operadores')
def plataforma(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        agua_tratada_grafico_vetor = []
        # Recupera os três últimos objetos do modelo Analise_Agua_tratada com base no campo 'id'
        agua_tratada_grafico = Analise_Agua_tratada.objects.order_by('-id')[:3]

        for item in agua_tratada_grafico:
            agua_tratada_grafico_vetor.append(item)

        # parametros pre estabelecidos no django-admin
        parametro = Parametro.objects.all()

        # busca aviso no banco de dados
        avisos = OperadoresAviso.objects.all()

        # buscar do banco a última análise para mostrar no HTML,
        # todos_operadores = User.objects.all()
        # quantidade_usuarios = todos_operadores.count()
        # print(f'quantidade de usuario:  {quantidade_usuarios}')

        ultimo_cal = Cal_Quantidade.objects.last()
        if ultimo_cal:
            ultimo_operador = ultimo_cal.operador
        else:
            ultimo_operador = 'Ninguém'

        ultimo_cal = Cal_Quantidade.objects.last()
        if ultimo_cal:
            ultimo_data = ultimo_cal.data
        else:
            ultimo_data = '???'

        # API clima agora
        API_KEY = "88b9a728f6d07c27fd1e204ce3237cc7"
        link_agora = f"https://api.openweathermap.org/data/2.5/weather?lat=-20.438&lon=-48.012&appid={API_KEY}&lang=pt_br"
        link_futuro = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=44.34&lon=10.99&appid={API_KEY}"

        requisicao_agora = requests.get(link_agora)
        requisicao_dic_agora = requisicao_agora.json()
        descricao_agora = requisicao_dic_agora['weather'][0]['description']
        temperatura = requisicao_dic_agora['main']['temp'] - 273.15
        temperatura_html = f'{temperatura:.2f}°C'

        if len(avisos) > 0:
            return render(request, 'plataforma.html', {'nome': nome,
                                                       'agua_tratada_grafico_vetor': agua_tratada_grafico_vetor,
                                                       'avisos': avisos,
                                                       'parametro': parametro,
                                                       'ultimo_operador': ultimo_operador,
                                                       'ultimo_data': ultimo_data,
                                                       'esta_autorizado': esta_autorizado,
                                                       'descricao_agora': descricao_agora,
                                                       'temperatura_html': temperatura_html,

                                                       })
        # sem avisos
        return render(request, 'plataforma.html', {'nome': nome,
                                                   'agua_tratada_grafico_vetor': agua_tratada_grafico_vetor,
                                                   'parametro': parametro,
                                                   'ultimo_operador': ultimo_operador,
                                                   'ultimo_data': ultimo_data,
                                                   'esta_autorizado': esta_autorizado,

                                                   })
    elif request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username

        return render(request, 'plataforma.html', {'nome': nome,
                                                   })


# Def que salva os dados da agua tratada
@login_required(login_url='operadores')
def agua_tratada(request):
    if request.method == 'GET':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        return render(request, 'agua_tratada.html', {'nome': nome,
                                                     'esta_autorizado': esta_autorizado,

                                                     })

    elif request.method == 'POST':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        cloro = request.POST.get('cloro')
        ph = request.POST.get('ph')
        fluor = request.POST.get('fluor')
        cor = request.POST.get('cor')
        turbidez = request.POST.get('turbidez')
        relatorio = request.POST.get('relatorio')

        if relatorio == '':
            relatorio = 'Nada consta'

        # Verifica se todos os campos do formulário foram preenchidos
        if not all([cloro, ph, cor, turbidez, fluor]):
            messages.error(request, 'Preencha todas as informações corretamente')
            return render(request, 'agua_tratada.html', {'nome': nome})

        # Tente salvar no banco
        try:

            analise_diaria = Analise_Agua_tratada(
                cloro=float(cloro),
                ph=float(ph),
                cor=float(cor),
                fluor=float(fluor),
                turbidez=float(turbidez),
                relatorio=relatorio,
                data_analise_agua=datetime.datetime.now(),
                usuario=request.user
            )

            analise_diaria.save()
            messages.success(request, 'Dados preenchidos corretamente')

            cloro = ''
            ph = ''
            cor = ''
            turbidez = ''
            relatorio = ''
            fluor = ''

        except Exception as e:
            # Função para verificar se uma string é um número
            def is_number(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False

            # Verificar e atribuir 'ERRO' se não forem números
            ph = 'ERRO' if not is_number(ph) else ph
            cor = 'ERRO' if not is_number(cor) else cor
            turbidez = 'ERRO' if not is_number(turbidez) else turbidez
            cloro = 'ERRO' if not is_number(cloro) else cloro
            fluor = 'ERRO' if not is_number(fluor) else fluor

            # Vamos imprimir o erro no console para depuração
            print("Erro ao salvar a análise:", e)
            messages.warning(request, 'Erro interno do sistema. Tente novamente.')
            messages.warning(request, 'Certifique-se de estar usando ponto em vez de vírgula, ex: "7.23" está correto')

        return render(request, 'agua_tratada.html', {'nome': nome,
                                                     'ph': ph,
                                                     'cloro': cloro,
                                                     'turbidez': turbidez,
                                                     'cor': cor,
                                                     'relatorio': relatorio,
                                                     'esta_autorizado': esta_autorizado,
                                                     'fluor': fluor,
                                                     })


# Def que salva os dados da agua bruta
@login_required(login_url='operadores')
def agua_bruta(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        return render(request, 'agua_bruta.html', {'nome': nome,
                                                   'esta_autorizado': esta_autorizado,
                                                   })

    elif request.method == 'POST':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        decantada_ph = request.POST.get('decantada_ph')
        decantada_cor = request.POST.get('decantada_cor')
        decantada_turbidez = request.POST.get('decantada_turbidez')

        bruta_ph = request.POST.get('bruta_ph')
        bruta_cor = request.POST.get('bruta_cor')
        bruta_turbidez = request.POST.get('bruta_turbidez')

        qeta = request.POST.get('qeta')
        qpac = request.POST.get('qpac')
        qcal = request.POST.get('qcal')

        relatorio = request.POST.get('relatorio')

        # se o numero se string no input HTML for melhor que zero então atribua esta frase para a varialvel
        if len(relatorio) < 1:
            relatorio = 'Nada consta'

        if len(qcal) < 1:
            qcal = 0
        # tente salvar no banco
        try:
            analise_diaria_bruta = Analise_Agua_bruta(
                decantada_ph=decantada_ph,
                decantada_cor=decantada_cor,
                decantada_turbidez=decantada_turbidez,
                bruta_ph=bruta_ph,
                bruta_cor=bruta_cor,
                bruta_turbidez=bruta_turbidez,
                relatorio=relatorio,
                qcal=qcal,
                qpac=qpac,
                qeta=qeta,
                data_analise_agua=datetime.datetime.now(),
                usuario=request.user  # Usuário logado atualmente
            )
            analise_diaria_bruta.save()
            messages.add_message(request, constants.SUCCESS, 'Dados preenchidos corretamente')

            return render(request, 'agua_bruta.html', {'nome': nome})

        # caso não seja possivel savar no banco imprima este avisa na tela (HTML)
        except Exception as e:

            # Imprimir o erro no console para depuração
            print("Erro ao salvar a análise:", e)
            messages.add_message(request, constants.WARNING,
                                 'Certifique-se que esteja usando ponto ao ivés de virgula ex: ''7.23 está correto''')
            messages.add_message(request, constants.WARNING,
                                 'Erro interno do sistema. Tente novamente. views.plataforma.agua_bruta')

            decantada_ph = request.POST.get('decantada_ph')
            decantada_cor = request.POST.get('decantada_cor')
            decantada_turbidez = request.POST.get('decantada_turbidez')

            bruta_ph = request.POST.get('bruta_ph')
            bruta_cor = request.POST.get('bruta_cor')
            bruta_turbidez = request.POST.get('bruta_turbidez')

            qeta = request.POST.get('qeta')
            qpac = request.POST.get('qpac')
            qcal = request.POST.get('qcal')

            # Função para verificar se uma string é um número
            def is_number(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False

            # Verificar e atribuir 'ERRO' se não forem números
            if not is_number(decantada_ph):
                decantada_ph = 'ERRO'
            if not is_number(decantada_cor):
                decantada_cor = 'ERRO'
            if not is_number(decantada_turbidez):
                decantada_turbidez = 'ERRO'

            if not is_number(bruta_ph):
                bruta_ph = 'ERRO'
            if not is_number(bruta_cor):
                bruta_cor = 'ERRO'
            if not is_number(bruta_turbidez):
                bruta_turbidez = 'ERRO'

            if not is_number(qeta):
                qeta = 'ERRO'
            if not is_number(qpac):
                qpac = 'ERRO'
            if not is_number(qcal):
                qcal = 'ERRO'

            relatorio = request.POST.get('relatorio')

            return render(request, 'agua_bruta.html', {'nome': nome,
                                                       'decantada_ph': decantada_ph,
                                                       'decantada_cor': decantada_cor,
                                                       'decantada_turbidez': decantada_turbidez,
                                                       'bruta_ph': bruta_ph,
                                                       'bruta_cor': bruta_cor,
                                                       'bruta_turbidez': bruta_turbidez,
                                                       'qeta': qeta,
                                                       'qpac': qpac,
                                                       'qcal': qcal,
                                                       'relatorio': relatorio,
                                                       'esta_autorizado': esta_autorizado,
                                                       })


# Def que salva os dados do cal consumido
@login_required(login_url='operadores')
def adicao_de_cal(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        # Obtém todos os objetos da tabela Tabela_estoque_cal
        cal_objs = Tabela_estoque_cal.objects.all()

        # Criando uma lista para armazenar os resultados divididos por 20 com // retira-se os décimos
        resultados_divididos = [cal.resultado_final // 20 for cal in cal_objs]

        for quilos_cal in resultados_divididos:
            quilos_cal

        quilos_cal = quilos_cal * 20

        return render(request, 'adicao_de_cal.html', {'nome': nome,
                                                      'resultados_divididos': resultados_divididos,
                                                      'quilos_cal': quilos_cal,
                                                      'esta_autorizado': esta_autorizado,

                                                      })

    elif request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username
        relatorio = request.POST.get('relatorio')

        if hasattr(nome, 'laboratorio'):
            esta_autorizado = nome.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        # Obtém todos os objetos da tabela Tabela_estoque_cal
        cal_objs = Tabela_estoque_cal.objects.all()

        for cal in cal_objs:
            # Calcula o novo valor de resultado_final subtraindo 20
            novo_valor = cal.resultado_final - 20
            # Atualiza o campo resultado_final no objeto atual
            cal.resultado_final = novo_valor
            # Salva o relatório no campo relatorio do objeto atual
            cal.relatorio = relatorio
            # Salva a atualização no banco de dados
            cal.save()

    # Obtém todos os objetos da tabela Tabela_estoque_cal
    cal_objs = Tabela_estoque_cal.objects.all()

    # Criando uma lista para armazenar os resultados divididos por 20 com // retira-se os décimos
    resultados_divididos = [cal.resultado_final // 20 for cal in cal_objs]
    if relatorio == '':
        relatorio = 'Nada Consta'
    q_cal = Cal_Quantidade(
        quantidade='1 saco de cal',
        data=datetime.datetime.now(),
        operador=request.user,  # Usuário logado atualmente
        relatorio=relatorio,
    )
    q_cal.save()
    for quilos_cal in resultados_divididos:
        quilos_cal

    quilos_cal = quilos_cal * 20

    messages.add_message(request, constants.SUCCESS, 'Cal adicionado com sucesso!')

    return render(request, 'adicao_de_cal.html', {'nome': nome,
                                                  'resultados_divididos': resultados_divididos,
                                                  'quilos_cal': quilos_cal,
                                                  })


# Def que salva a 'produção' de agua limpa
@login_required(login_url='operadores')
def hidrometro(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        # buscar os ultimos dados salvos e reproduzir no bootstrap html

        return render(request, 'hidrometro.html', {'nome': nome,
                                                   'esta_autorizado': esta_autorizado,

                                                   })

    elif request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username

        if hasattr(nome, 'laboratorio'):
            esta_autorizado = nome.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        hidrometro_150 = request.POST.get('hidrometro_150')
        hidrometro_200 = request.POST.get('hidrometro_200')
        hidrometro_poco = request.POST.get('hidrometro_poco')
        relatorio = request.POST.get('relatorio')

        if relatorio == '':
            relatorio = 'Nada Consta'

        print(hidrometro_200)
        try:
            hidro = Hidrometro(
                hidrometro_150=hidrometro_150,
                hidrometro_200=hidrometro_200,
                hidrometro_poco=hidrometro_poco,
                operador=request.user,
                data=datetime.datetime.now(),
                relatorio=relatorio,
            )
            hidro.save()

            hidrometro_150 = ''
            hidrometro_200 = ''
            hidrometro_poco = ''
            relatorio = ''

            messages.add_message(request, constants.SUCCESS, 'Dados preenchidos corretamente')

        # caso não seja possivel savar no banco imprima este aviso na tela (HTML)
        except Exception as e:

            # Imprimir o erro no console para depuração
            print("Erro ao salvar a análise:", e)
            messages.add_message(request, constants.WARNING,
                                 'Certifique-se que esteja usando ponto ao ivés de virgula ex: ''7.23 está correto''')
            messages.add_message(request, constants.WARNING,
                                 'Erro interno do sistema. Tente novamente. views.plataforma.hidrometro')

            # Função para verificar se uma string é um número
            def is_number(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False

            # Verificar e atribuir 'ERRO' se não forem números
            if not is_number(hidrometro_150):
                hidrometro_150 = 'ERRO'
            if not is_number(hidrometro_200):
                hidrometro_200 = 'ERRO'
            if not is_number(hidrometro_poco):
                hidrometro_poco = 'ERRO'

    return render(request, 'hidrometro.html', {'nome': nome,
                                               'hidrometro_150': hidrometro_150,
                                               'hidrometro_200': hidrometro_200,
                                               'hidrometro_poco': hidrometro_poco,
                                               'relatorio': relatorio,
                                               })


# Def que salva a saida dos caminhoes que buscam água limpa
@login_required(login_url='operadores')
def saida_de_caminhao_pipa(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        return render(request, 'saida_de_caminhao_pipa.html', {'nome': nome,
                                                               'esta_autorizado': esta_autorizado,
                                                               })

    elif request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username

        if hasattr(nome, 'laboratorio'):
            esta_autorizado = nome.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        placa = request.POST.get('placa')
        motorista = request.POST.get('motorista')
        quantidade = request.POST.get('quantidade')
        destino = request.POST.get('destino')
        relatorio = request.POST.get('relatorio')

        if placa == '':
            placa = 'Placa não informada'
        if destino == '':
            destino = 'Destino não informado'
        if relatorio == '':
            relatorio = 'Nada consta'
        if motorista == '':
            motorista = 'Motorista não informado'
        if len(quantidade) > 0:

            caregado = SaidaCaminhaPipa(
                data=datetime.datetime.now(),
                operador=request.user,
                relatorio=relatorio,
                placa=placa,
                destino=destino,
                motorista=motorista,
                quantidade=quantidade,
            )
            caregado.save()

            messages.add_message(request, constants.SUCCESS, 'Dados preenchidos corretamente')

            # neste caso em especial não um o Try
            # fiz a usei o if da verificação da quantidade como se fosse o Try
            # porque não julguei nescesário já que u if e o Try são parecedos
            # e ja ia ter que fazer as verificações com o if/elif
            # achei que assim o código ficou mais limpo, a idéia de um Try
            # dentro do if não me agradou

            # caso não seja possivel savar no banco imprima este avisa na tela (HTML)
        elif len(quantidade) <= 0:

            # Imprimir o erro no console para depuração
            print("Erro ao salvar a análise:")
            messages.add_message(request, constants.WARNING,
                                 'Digite a quantidade de litros de agua ou '
                                 'certifique-se que esteja usando ponto ao ivés de virgula ex: ''7.23 está correto''')
            messages.add_message(request, constants.WARNING,
                                 'Erro interno do sistema. Tente novamente. views.plataforma.saida_de_caminhao_pipa')

        return render(request, 'saida_de_caminhao_pipa.html', {'nome': nome})


# Def que trabalha com as mensagens deixadas pelos operadores
@login_required(login_url='operadores')
def mensagem(request):
    if request.method == 'GET':
        nome = request.user

        nome2 = request.user
        if hasattr(nome2, 'laboratorio'):
            esta_autorizado = nome2.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        # buscar do banco as mensagens
        # Recupere todas as mensagens ordenadas de forma decrescente pela data e hora de criação
        buscar_msg = Mensagem.objects.all().order_by('-id')[:7]

        data = Mensagem.objects.last().data

        return render(request, 'mensagem.html', {'nome': nome,
                                                 'buscar_msg': buscar_msg,
                                                 'data': data,
                                                 'esta_autorizado': esta_autorizado,

                                                 })
    elif request.method == 'POST':
        # Obtém o nome de usuário do usuário logado
        nome = request.user.username

        if hasattr(nome, 'laboratorio'):
            esta_autorizado = nome.laboratorio.autorizado
            print(esta_autorizado)
        else:
            esta_autorizado = False
            print(esta_autorizado)

        msg = request.POST.get('msg')

        try:

            envio_msg = Mensagem(
                data=datetime.datetime.now(),
                operador=request.user,
                mensagem=msg
            )
            if msg == '':
                messages.add_message(request, constants.WARNING,
                                     'Você precisa digitar sua mensagem antes de publicar')
                # buscar do banco as mensagens
                # Recupere todas as mensagens ordenadas de forma decrescente pela data e hora de criação
                buscar_msg = Mensagem.objects.all().order_by('-id')[:7]

                data = Mensagem.objects.last().data
                return render(request, 'mensagem.html', {'nome': nome,
                                                         'buscar_msg': buscar_msg,
                                                         'data': data,
                                                         })
            envio_msg.save()

            # caso não seja possivel savar no banco imprima este aviso na tela (HTML)
        except Exception as e:

            # para depuraçao do código
            print(e)

            messages.add_message(request, constants.WARNING,
                                 'Erro interno do sistema. Tente novamente. views.Mensagem')

        # buscar do banco as mensagens
        # Recupere todas as mensagens ordenadas de forma decrescente pela data e hora de criação
        buscar_msg = Mensagem.objects.all().order_by('-id')[:7]

        data = Mensagem.objects.last().data
        return render(request, 'mensagem.html', {'nome': nome,
                                                 'buscar_msg': buscar_msg,
                                                 'data': data,
                                                 })


def logout_view(request):
    logout(request)
    # Redirecione para onde você deseja após o logout
    return redirect('operadores')
