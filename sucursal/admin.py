from django.contrib import admin
from .models import Sucursal

# Configuración personalizada para la tabla Sucursal
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'telefono', 'direccion', 'status')
    search_fields = ('nombre', 'ciudad', 'direccion')
    list_filter = ('ciudad', 'status')
    ordering = ('id',)
    filter_horizontal = ('personal',)  # Widget pro para seleccionar los empleados fácilmente

# Registro formal en el sitio de Admin
admin.site.register(Sucursal, SucursalAdmin)