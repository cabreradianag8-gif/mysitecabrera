from django.urls import path
from . import views

urlpatterns = [
    # Consultar y Listar
    path('pageusuarios/', views.pageusuarios, name='rutapageusuarios'),
    
    # Crear
    path('usuarios/nuevo/', views.nuevo_usuario, name='nuevo_usuario'),
    
    # Editar / Actualizar
    path('usuarios/actualizar/<int:usuario_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    
    #  Cambiar Estatus 
    path('usuarios/estatus/<int:usuario_id>/', views.cambiar_estatus_usuario, name='cambiar_estatus_usuario'),
]