from calendar import TUESDAY
from django.db import models
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
# Modelos Kiltros pet shop

# Create Modelo para Categoria

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name="Id de categoría")
    nombreCategoria = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la categoría")

    def __str__(self):
        return self.nombreCategoria  


class Estado(models.Model):
    idEstado = models.IntegerField(primary_key=True, verbose_name="Id de Estado")
    nombreEstado = models.CharField(max_length=80, blank=False, null=False, verbose_name="Tipo de estado")

    def __str__(self):
        return self.nombreEstado

class Tipo_usuario(models.Model):
    idTipo = models.IntegerField(primary_key=True, verbose_name="Id de tipo de usuario")
    nombreTipo = models.CharField(max_length=80, blank=False, null=False, verbose_name="Tipo de usuario")

    def __str__(self):
        return self.nombreTipo

# Create Modelo para Mantenedor de Producto

class Producto(models.Model):
    id = models.CharField(max_length=6, primary_key=True, verbose_name="Id de producto")
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    nombre =  models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre")
    descripcion =  models.CharField(max_length=80, blank=False, null=False, verbose_name="Descripción")
    precio =  models.CharField(max_length=80, blank=False, null=False, verbose_name="Precio")
    descuentosub =  models.CharField(max_length=80, blank=True, null=True, verbose_name="Descuento subscriptor")
    descuentoferta =  models.CharField(max_length=80, blank=True, null=True, verbose_name="Descuento por oferta")
    cantidad =  models.CharField(max_length=80, blank=False, null=True, verbose_name="Cantidad")
    imagen = models.ImageField(upload_to="images/", default="sinfoto.jpg", null=True, blank=True, verbose_name="Imagen")
    def __str__(self):
        return self.nombre          

# Create Modelo para Factura

class Factura(models.Model):
    Nro_factura = models.CharField(max_length=6, primary_key=True, verbose_name="Id de producto")
    fecha = models.DateTimeField(verbose_name = "Fecha")
    nombre_cliente =  models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre")
    monto_total = models.CharField(max_length=80, blank=False, null=False, verbose_name="Monto total")
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.nombre       


class PerfilUsuario(models.Model):
    
    tipo_usuario = models.ForeignKey(Tipo_usuario, on_delete=models.DO_NOTHING, null= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=80, blank=True, null=True, verbose_name="Rut")
    direccion = models.CharField(max_length=80, blank=True, null=True, verbose_name="Dirección")
    imagen = models.ImageField(upload_to="images/", default="sinfoto.jpg", null=True, blank=True, verbose_name="Imagen")
    sub = models.BooleanField(blank=True, null=True, verbose_name="sub")
    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name} ({self.user.email})"