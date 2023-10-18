from django.urls import path
from . import views

urlpatterns = [
    path('plataforma/', views.plataforma, name='plataforma'),
    path('plataforma/agua_tratada/', views.agua_tratada, name='agua_tratada'),
    path('plataforma/agua_bruta/', views.agua_bruta, name='agua_bruta'),
    path('plataforma/adicao_de_cal/', views.adicao_de_cal, name='adicao_de_cal'),
    path('plataforma/hidrometro/', views.hidrometro, name='hidrometro'),
    path('plataforma/saida_de_caminhao_pipa/', views.saida_de_caminhao_pipa, name='saida_de_caminhao_pipa'),
    path('plataforma/mensagem/', views.mensagem, name='mensagem'),

]
