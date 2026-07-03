from django.urls import path
from .views import listaempleados, createempleados

urlpatterns = [
    path('', listaempleados),
    path('nuevo/', createempleados)
]
