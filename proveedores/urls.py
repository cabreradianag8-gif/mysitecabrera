from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageproveedores, name='pageproveedores'), 
    path('editar/<int:pk_editar>/', views.pageproveedores, name='preparar_editar_prov'),
    path('nuevo/', views.nuevo_proveedor, name='nuevo_proveedor'),
    path('actualizar/<int:pk>/', views.actualizar_proveedor, name='actualizar_provider'), 
    path('eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('reactivar/<int:pk>/', views.reactivar_proveedor, name='reactivar_proveedor'),
]