from django.urls import path
from .views import listaproductos, createproductos


urlpatterns = [
    path('',listaproductos),
    path('nuevo/',createproductos)
]