import imp
from unicodedata import name
from django.urls import path, include
from .views import index, carrito, contacto, donacion, Editusuario, Factura_admin, Factura, Historial_compra, iniciar_sesion, ficha, iniciar_pago,pago_exitoso
from .views import Mantenedor_productos, Mantenedor_bodega, nosotros, Perfil_Usuario, productos, registrar_usuario, rifa, seguimiento, Venta, ProductoViewset, PerfilUsuarioViewset              
from rest_framework import routers


router = routers.DefaultRouter()
router.register('productos', ProductoViewset)

router2 = routers.DefaultRouter()
router2.register('clientes', PerfilUsuarioViewset)


urlpatterns = [
    path('',index, name='index'),
    path('carrito', carrito, name='carrito'),
    path('contacto', contacto, name='contacto'),
    path('donacion', donacion, name='donacion'),
    path('Editusuario/<action>/<id>', Editusuario, name='Editusuario'),
    path('Factura_admin', Factura_admin, name='Factura_admin'),
    path('Factura', Factura, name='Factura'),
    path('ficha/<id>', ficha, name="ficha"),
    path('Historial_compra', Historial_compra, name='Historial_compra'),
    path('login', iniciar_sesion, name='login'),
    path('Mantenedor_productos/<action>/<id>', Mantenedor_productos, name='Mantenedor_productos'),
    path('Mantenedor_bodega/<action>/<id>', Mantenedor_bodega, name='Mantenedor_bodega'),
    path('nosotros', nosotros, name='nosotros'),
    path('Perfil_Usuario/', Perfil_Usuario, name='Perfil_Usuario'),
    path('productos', productos, name='productos'),
    path('pago_exitoso/<id>', pago_exitoso, name="pago_exitoso"),
    path('registrarte', registrar_usuario, name='registrarte'),
    path('rifa', rifa, name='rifa'),
    path('seguimiento', seguimiento, name='seguimiento'),
    path('Venta', Venta, name='Venta'),
    path('api/', include (router.urls)),
    path('api/', include (router2.urls)),
    path('seguimiento', seguimiento, name='seguimiento'),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),


]
