from django.shortcuts import render, redirect
from pagina_inicial.models import Reclame, Aviso, Contato
from django.contrib import messages
from django.contrib.messages import constants


def index(request):
    if request.method == 'GET':

        # buscar no banco todas as postagem ja disponibilizadas
        # estas postagem é referente a classe Aviso do arquivo models.py
        # para criar um Aviso usa-se o admin do django
        # depois de criadas no admin buscamos no banco e reenderizamos no html
        postagem = Aviso.objects.all()

        publicar_reclame = Reclame.objects.filter(boolean=True).order_by('-id')[:10]

        objeto = Contato.objects.all().order_by('-id')[:1]  # busca do banco 1 valor apenas

        # este bloco é importante para garantir que o sistema vai rodar
        #  primeira vez sem erro, Acaso dê erro o ADM cadastrsdo vai ter
        # que preencher manualmete na area Django-Admin, para rodar a primeira vez
        tel = None
        cidade_estado = None
        email = None
        ###############################################################################

        for item in objeto:
            tel = item.telefone
            cidade_estado = item.cidade_estado
            email = item.email

        return render(request, 'index.html', {'postagem': postagem,
                                              'publicar_reclame': publicar_reclame,
                                              'tel': tel,
                                              'cidade_estado': cidade_estado,
                                              'email': email,

                                              })
    elif request.method == 'POST':
        mensagem = request.POST.get('mensagem').strip()
        nome = request.POST.get('nome').strip()
        rua = request.POST.get('rua').strip()
        email_ou_tel = request.POST.get('email_ou_tel').strip()
        recado = Reclame(mensagem=mensagem, nome=nome, rua=rua, email_ou_tel=email_ou_tel)

        # Se não existe mensagem, não faça nada
        if not mensagem:
            messages.add_message(request, constants.ERROR, '!Mensagem Inválida! preencha uma mensagem')
            return redirect('index')
        if len(rua) < 8:
            messages.add_message(request, constants.ERROR,
                                 '!Mensagem Inválida! Preencha uma Rua ou Avenida válido com o número da residência')
            return redirect('index')
        else:
            try:
                recado.save()
                messages.add_message(request, constants.SUCCESS, 'Sucesso! Logo mais você será respondido')

            except:
                # Não foi possível salvar o recado
                messages.add_message(request, constants.WARNING,
                                     'Erro interno do sistema, tente de novo! views.pagina_inicial.index')

        # Redirecionamento para a própria página
        return redirect('index')
