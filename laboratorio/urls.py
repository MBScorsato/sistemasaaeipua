from django.urls import path
from . import views

urlpatterns = [
    path('laboratorio/', views.laboratorio, name='laboratorio'),
    path('laboratorio/analises/basica/interna', views.analises_basica_interna, name='analises_basica_interna'),

]