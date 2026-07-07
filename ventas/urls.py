from django.urls import path
from .views import listaventas, createventas

urlpatterns = [
    path('', listaventas),
    path('nuevo/', createventas),
]