from django.contrib import admin
from .models import empleados

# Configuración personalizada para la tabla empleados
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'departamento', 'telefono', 'email', 'turno', 'status')
    search_fields = ('nombre', 'apellido', 'email', 'departamento')
    list_filter = ('departamento', 'turno', 'status')
    ordering = ('id',)

# Registro formal en el sitio de Admin
admin.site.register(empleados, EmpleadosAdmin)