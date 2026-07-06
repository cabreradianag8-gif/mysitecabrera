from django.urls import path
from . import views

urlpatterns = [
    # Al dejar las comillas vacías '', indicamos que esta es la raíz de la app
    path('', views.home , name='home'),
]
