from django.urls import path
from . import views

urlpatterns = [
    path('form-productos', views.productos),
]