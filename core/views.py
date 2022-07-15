from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import  Producto, PerfilUsuario
from .forms import ProductoForm, BodegaForm, EditForm, RegistrarUsuarioForm, PerfilUsuarioForm, IniciarSesionForm
from django.views.decorators.csrf import csrf_exempt
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import random

#rest_framework
from rest_framework import viewsets
from .serializers import ProductoSerializer
from .serializers import PerfilUsuarioSerializer


# Create your views here.

def index(request):
    return render(request, "core/index.html")

@csrf_exempt
def iniciar_pago(request, id):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = Producto.objects.get(id=id).precio
    return_url = 'http://127.0.0.1:8000/pago_exitoso/'+ id

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url )
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "direccion": perfil.direccion,
        
    }

    return render(request, "core/iniciar_pago.html", context)

#https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
#https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
#https://www.transbankdevelopers.cl/referencia/webpay

# Tipo de tarjeta   Detalle                        Resultado
#----------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)


@csrf_exempt
def pago_exitoso(request, id):

    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)
        form = PerfilUsuarioForm()
        producto = Producto.objects.get(id=id)

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rut": perfil.rut,
            "direccion": perfil.direccion,
            "response_code": response['response_code'],
            "producto": producto
            
        }
        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect(index)

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(index)
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "registration/login.html", data )
    
def carrito(request):
    return render(request, "core/carrito.html" )

def contacto(request):
    return render(request, "core/contacto.html" )

def donacion(request):
    return render(request, "core/donacion.html" )


def Editusuario(request, action, id):
    data = {"mesg": "", "form": EditForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = EditForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El Usuario fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos Usuarios con el mismo id!"

    elif action == 'upd':
        objeto = PerfilUsuario.objects.get(user=id)
        if request.method == "POST":
            form = EditForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El Usuario fue actualizado correctamente!"
        data["form"] = EditForm(instance=objeto)

    elif action == 'del':
        try:
            PerfilUsuario.objects.get(user=id).delete()
            data["mesg"] = "¡El Usuario fue eliminado correctamente!"
            return redirect(PerfilUsuario, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El Usuario ya estaba eliminado!"

    
    data["list"] = PerfilUsuario.objects.all().order_by('user')
    return render(request, "core/Editusuario.html", data )

def Factura_admin(request):
    return render(request, "core/Factura_admin.html" )

def Factura(request):
    return render(request, "core/Factura.html" )

@csrf_exempt
def ficha(request, id):
    data = {"mesg": "", "producto": None}

    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(iniciar_pago, id)
        else:
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    data["producto"] = Producto.objects.get(id=id)
    return render(request, "core/ficha.html", data)
    
def Historial_compra(request):
    return render(request, "core/Historial_compra.html" )

def Mantenedor_productos(request, action, id):
    data = {"mesg": "", "form": ProductoForm, "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El Producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos Productos con el mismo id!"

    elif action == 'upd':
        objeto = Producto.objects.get(id=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El Producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(id=id).delete()
            data["mesg"] = "¡El Producto fue eliminado correctamente!"
            return redirect(Producto, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El Producto ya estaba eliminado!"

    
    data["list"] = Producto.objects.all().order_by('nombre')
    return render(request, "core/Mantenedor_productos.html", data )


def Mantenedor_bodega(request, action, id):
    data = {"mesg": "", "form": BodegaForm, "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = BodegaForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El Producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos Productos con el mismo id!"

    elif action == 'upd':
        objeto = Producto.objects.get(id=id)
        if request.method == "POST":
            form = BodegaForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El Producto fue actualizado correctamente!"
        data["form"] = BodegaForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(id=id).delete()
            data["mesg"] = "¡El Producto fue eliminado correctamente!"
            return redirect(Mantenedor_bodega, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El Producto ya estaba eliminado!"

    
    data["list"] = Producto.objects.all().order_by('nombre')
    return render(request, "core/Mantenedor_bodega.html", data)

def nosotros(request):
    return render(request, "core/nosotros.html" )


def productos(request):
    data = {"list": Producto.objects.all().order_by('id')}
    return render(request, "core/productos.html", data)

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            imagen = request.FILES.get("Imagen")
            sub = request.POST.get("sub")
            if sub == 'on':
                sub = True
            else:
                sub = False

            PerfilUsuario.objects.update_or_create(user=user, rut=rut, direccion=direccion, imagen = imagen, sub = sub)

            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    return render(request, "registration/registrarte.html", context={'form': form})

def rifa(request):
    return render(request, "core/rifa.html" )

def seguimiento(request):
    return render(request, "core/seguimiento.html" )


def Venta(request):
    return render(request, "core/Venta.html" )

def Perfil_Usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.direccion = request.POST.get("direccion")
            perfil.sub = request.POST.get("Subscripción")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['direccion'].initial = perfil.direccion
    form.fields['sub'].initial = perfil.sub
    data["form"] = form
    return render(request, "core/Perfil_Usuario.html", data)


class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer



class PerfilUsuarioViewset(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer            