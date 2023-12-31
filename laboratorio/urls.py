from django.urls import path
from . import views

urlpatterns = [
    path('laboratorio/', views.laboratorio, name='laboratorio'),
    path('laboratorio/controle/operacional/analises/basica/interna', views.analises_basica_interna,
         name='analises_basica_interna'),
    path('laboratorio/controle/operacional', views.controle_operacional, name='controle_operacional'),
    path('laboratorio/controle/operacional/reservatorio', views.reservatorio, name='reservatorio'),
    path('laboratorio/controle/operacional/calculadora', views.calculadora, name='calculadora'),
    path('laboratorio/controle/operacional/anotacoes/gerais', views.anotacoes_gerais, name='anotacoes_gerais'),
    path('laboratorio/controle/operacional/ver/anotacoes/', views.ver_anotacoes, name='ver_anotacoes'),
    path('laboratorio/controle/operacional/organizador/tarefas', views.organizador_tarefas, name='organizador_tarefas'),
    path('laboratorio/controle/operacional/organizador/tarefas/aberta', views.tarefas_aberta, name='tarefas_aberta'),
    path('laboratorio/sair/', views.logout_view, name='logout_view'),

]
