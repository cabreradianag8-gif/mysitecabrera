from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagecompras, name='rutapagecompras'),
    path('registrar/', views.registrar_compra, name='registrar_compra'),
    path('cancelar/<int:pk>/', views.cancelar_compra, name='cancelar_compra'),
]