from django.urls import path
from . import views

urlpatterns = [
    # Consultar y Listar
    path('pagegrupos/', views.pagegrupos, name='rutapagegrupos'),
    
    # Crear
    path('grupos/nuevo/', views.nuevo_grupo, name='nuevo_grupo'),
    
    # Editar / Actualizar
    path('grupos/actualizar/<int:grupo_id>/', views.actualizar_grupo, name='actualizar_grupo'),
    
    # Desactivar / Reactivar (Cambio de estatus)
    path('grupos/estatus/<int:grupo_id>/', views.cambiar_estatus_grupo, name='cambiar_estatus_grupo'),
]