from django.urls import path
from .views import listaclientes, createclientes

urlpatterns = [
    path('', listaclientes),
    path('nuevo/', createclientes)
]
