from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),

    # Rota padrão que redireciona para a função plataforma
    path('', views.index, name='index'),
]
