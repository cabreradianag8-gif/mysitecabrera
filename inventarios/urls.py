from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageinventarios, name='rutapageinventarios'),
    path('editar/<int:pk_editar>/', views.pageinventarios, name='editar_inventario'),
    path('nuevo/', views.nuevo_inventario, name='nuevo_inventario'),
    path('actualizar/<int:pk>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('eliminar/<int:pk>/', views.eliminar_inventario, name='eliminar_inventario'),
    
    # NUEVA RUTA: Para sacar el stock de la papelera
    path('restaurar/<int:pk>/', views.restaurar_inventario, name='restaurar_inventario'),
]