from django.contrib import admin
from .models import Categoria,Producto, PerfilUsuario, Tipo_usuario

# Register your models here.

admin.site.register(Categoria)
#admin.site.register(Vehiculo)
admin.site.register(Producto)
admin.site.register(Tipo_usuario)
admin.site.register(PerfilUsuario)