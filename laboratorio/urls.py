from django.urls import path
from . import views

urlpatterns = [
    path('laboratorio/', views.laboratorio, name='laboratorio'),

]
