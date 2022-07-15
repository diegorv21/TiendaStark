from dataclasses import fields
#Aqui empieza codigo para la api
from rest_framework import serializers
from .models import Producto
from .models import PerfilUsuario
from .models import User

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id', 'categoria', 'nombre', 'descripcion', 'precio', 'descuentosub', 'descuentoferta']



class PerfilUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerfilUsuario
        fields = ['id', 'tipo_usuario', 'user', 'rut', 'direccion', 'sub']        