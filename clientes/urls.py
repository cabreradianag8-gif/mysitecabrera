from django.urls import path
from . import views

urlpatterns = [
    path('form-clientes', views.clientes),
]