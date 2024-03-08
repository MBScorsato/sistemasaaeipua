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
    path('laboratorio/residencias', views.residencias, name='residencias'),
    path('laboratorio/index_relatorio/particulares/externas', views.relatorios, name='relatorios'),
    path('laboratorio/pdf_relatorio/<int:pk>/id_pdf', views.pdf_relatorio, name='pdf_relatorio'),
    path('laboratorio/patrimonio/cadastrado/saae', views.patrimonio_cadastrado, name='patrimonio_cadastrado'),
    path('laboratorio/index_relatorio/pdf', views.index_relatorio, name='index_relatorio'),
    path('laboratorio/index_relatorio/monitoramento/diario/pdf', views.monitoramento_diario, name='monitoramento_diario'),
    path('laboratorio/index_relatorio/eficiencia/eta/pdf', views.eficiencia_eta, name='eficiencia_eta'),
    path('laboratorio/index_relatorio/hidrometro/pdf', views.relatorio_hidrometro, name='relatorio_hidrometro'),

]
