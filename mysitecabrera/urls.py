"""
URL configuration for mysitecabrera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('pageclientes/', include('clientes.urls')),
    path('pageproveedores/', include('proveedores.urls')),
    path('pageproductos/', include('productos.urls')),
    path('pageusuarios/', include('usuarios.urls')),
    path('pageempleados/', include('empleados.urls')),
    path('pagecompras/', include('compras.urls')),
    path('pageventas/', include('ventas.urls')),
]
 