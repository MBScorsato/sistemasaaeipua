from django.urls import path
from . import views


urlpatterns = [
    path('operadores/', views.operadores, name='operadores')

]