from django.http import HttpResponse
from django.shortcuts import render
from plataforma.models import Laboratorio


def laboratorio(request):
    if request.method == 'GET':
        # Obtém o usuário logado
        usuario = request.user

        # Verifica se o usuário tem um relacionamento com o modelo Laboratorio
        if hasattr(usuario, 'laboratorio'):
            laboratorio = usuario.laboratorio

            # Verifica o campo 'autorizado' do modelo Laboratorio
            esta_autorizado = laboratorio.autorizado

            if not esta_autorizado:
                return HttpResponse('<h1>Você tentou acessar de forma não permitida, hahahaha, tente outra vez!</h1>')
        else:
            return HttpResponse('<h1>Você não tem permissão para acessar esta página.</h1>')

        return render(request, 'laboratorio.html')

    elif request.method == 'POST':
        return render(request, 'laboratorio.html')
