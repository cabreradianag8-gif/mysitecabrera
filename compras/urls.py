from django.urls import path
from .views import listacompras, createcompras

urlpatterns = [
    path('', listacompras),
    path('nuevo/', createcompras)
]