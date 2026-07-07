from django.urls import path
from .views import listausuarios, createusuarios, creategrupos # <-- Añadimos creategrupos

urlpatterns = [
    path('', listausuarios),
    path('nuevo/', createusuarios),
    path('nuevogrupo/', creategrupos), # <-- Ruta para procesar el formulario de grupos
]
