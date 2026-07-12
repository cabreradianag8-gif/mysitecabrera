from django.urls import path
from . import views

urlpatterns = [
    path('', views.modulo_ventas_view, name='rutapageventas'),
    path('nueva/', views.nueva_venta, name='nueva_venta'),
    path('cancelar/<int:pk>/', views.cancelar_venta, name='cancelar_venta'),
]