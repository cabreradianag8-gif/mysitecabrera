from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageempleados_view, name='rutapageempleados'), 
    path('editar/<int:pk_editar>/', views.pageempleados_view, name='preparar_editar_empl'),
    path('nuevo/', views.nuevo_empleado, name='nuevo_empleado'),
    path('actualizar/<int:pk>/', views.actualizar_empleado, name='actualizar_empl_ejecutar'),
    path('eliminar/<int:pk>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('reactivar/<int:pk>/', views.reactivar_empleado, name='reactivar_empleado'),
]