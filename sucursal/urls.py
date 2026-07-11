from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagesucursal_view, name='rutapagesucursal'), 
    path('editar/<int:pk_editar>/', views.pagesucursal_view, name='preparar_editar_suc'),
    path('nuevo/', views.nueva_sucursal, name='nueva_sucursal'),
    path('actualizar/<int:pk>/', views.actualizar_sucursal, name='actualizar_suc_ejecutar'),
    path('eliminar/<int:pk>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('reactivar/<int:pk>/', views.reactivar_sucursal, name='reactivar_sucursal'),
]