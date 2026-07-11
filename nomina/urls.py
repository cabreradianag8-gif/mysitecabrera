from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagenomina_view, name='rutapagenomina'), 
    path('editar/<int:pk_editar>/', views.pagenomina_view, name='preparar_editar_nom'),
    path('nuevo/', views.nueva_nomina, name='nuevo_nomina'),
    path('actualizar/<int:pk>/', views.actualizar_nomina, name='actualizar_nom_ejecutar'),
    path('eliminar/<int:pk>/', views.eliminar_nomina, name='eliminar_nomina'),
    path('reactivar/<int:pk>/', views.reactivar_nomina, name='reactivar_nomina'),
]