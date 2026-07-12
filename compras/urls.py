from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagecompras_view, name='rutapagecompras'), 
    path('nuevo/', views.nueva_compra, name='nueva_compra'),
    path('cancelar/<int:pk>/', views.cancelar_compra, name='cancelar_compra'),
]