from django.shortcuts import render
from eta.models import EtaMidia


def eta(request):
    if request.method == 'GET':
        eta = EtaMidia.objects.all().order_by('-id')
        return render(request, 'eta.html', {'eta': eta})

    elif request.method == 'POST':
        return render(request, 'eta.html')