from django.urls import path
from .views import listausuarios, createusuarios


urlpatterns = [
    path('',listausuarios),
    path('nuevo/',createusuarios)
]