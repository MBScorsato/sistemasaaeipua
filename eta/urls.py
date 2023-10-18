from django.urls import path
from . import views

urlpatterns = [
    path('eta/', views.eta, name='eta')
]
