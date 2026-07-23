from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'estatus')
    search_fields = ('nombre', 'descripcion', 'categoria')
    list_filter = ('categoria', 'estatus')
    ordering = ('id',)


admin.site.register(Producto, ProductoAdmin)