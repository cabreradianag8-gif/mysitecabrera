from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageproductos, name='rutapageproductos'), 
    path('editar/<int:pk_editar>/', views.pageproductos, name='preparar_editar_prod'),
    path('nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_prod_ejecutar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('reactivar/<int:pk>/', views.reactivar_producto, name='reactivar_producto'),
]