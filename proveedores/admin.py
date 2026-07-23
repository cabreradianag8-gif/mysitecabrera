from django.contrib import admin
from .models import Proveedores

class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'telefono', 'email', 'direccion', 'estatus')
    search_fields = ('nombre', 'categoria', 'email', 'direccion')
    list_filter = ('categoria', 'estatus')
    ordering = ('id',)


admin.site.register(Proveedores, ProveedoresAdmin)