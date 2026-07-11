from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageclientes, name='pageclientes'), 
    path('editar/<int:pk_editar>/', views.pageclientes, name='preparar_editar'), # <-- Nueva: Carga los datos en el formulario
    path('nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
    path('actualizar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'), # <-- Procesa el cambio
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('reactivar/<int:pk>/', views.reactivar_cliente, name='reactivar_cliente'),
]