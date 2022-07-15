from pyexpat import model
from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria, PerfilUsuario, Producto 
from django.db import models
class ProductoForm(ModelForm):
    
    class Meta:
        model = Producto
        fields = ['id', 'categoria', 'nombre', 'descripcion', 'precio', 'descuentosub','descuentoferta', 'imagen' ]
        
class BodegaForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['id', 'categoria', 'nombre', 'cantidad' ]
        
class IniciarSesionForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class EditForm(ModelForm):
    id = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        model=PerfilUsuario
        fields='__all__'

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=80, required=True, label="Rut")
    direccion = forms.CharField(max_length=80, required=True, label="Dirección")
    sub = forms.BooleanField( label="Subscripción", required= False )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rut', 'direccion', 'sub']

class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=80, required=False, label="Rut")
    direccion = forms.CharField(max_length=80, required=False, label="Dirección")
    sub = forms.BooleanField( label="Subscripción", required= False)
    class Meta:
        model = PerfilUsuario
        fields = '__all__'