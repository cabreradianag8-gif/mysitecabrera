from django.urls import path
from . import views

urlpatterns = [
    # Consultar y Listar (Buscador + Paginación)
    path('pageinventarios/', views.pageinventarios, name='rutapageinventarios'),
    
    # Crear nueva combinación de stock
    path('inventarios/nuevo/', views.nuevo_inventario, name='nuevo_inventario'),
    
    # Editar / Actualizar stock local
    path('inventarios/actualizar/<int:inventario_id>/', views.actualizar_inventario, name='actualizar_inventario'),
    
    # Eliminar registro de inventario (Borrado físico o control)
    path('inventarios/eliminar/<int:inventario_id>/', views.eliminar_inventario, name='eliminar_inventario'),
]