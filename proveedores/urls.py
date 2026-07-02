from django.urls import path
from .views import listaproveedores, createproveedores


urlpatterns = [
    path('',listaproveedores),
    path('nuevo/',createproveedores)
]