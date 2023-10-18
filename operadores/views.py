from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import constants


# def que chama a area de login do sistema
def operadores(request):
    if request.method == 'GET':
        return render(request,  'operadores.html')
    elif request.method == 'POST':
        username = request.POST.get('nome')
        senha = request.POST.get('senha')

        # para cadastro usa-se a área do admin-django
        # só é possível cadastrar através da area admistrativa
        # essa variavel user receb o que foi cadastrado na área admin-django
        # é comparado os atributos e atribuidos na vari´vel user
        # a variável user so será True se username e password for igual ao digitado no html
        user = authenticate(username=username, password=senha)

        # caso seja True o user entrará neste if
        if user:
            login(request, user)
            return redirect('/plataforma')
        # senão (user False)
        else:
            messages.add_message(request, constants.ERROR, '!Erro! Senha ou Nome inválido!')
            return render(request, 'operadores.html')