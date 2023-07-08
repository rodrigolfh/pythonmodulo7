
from django.utils import timezone
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Categoria, Cliente, Pedido, Producto, ItemPedido
from .forms import RegistrarUsuarioForm, PedidoForm, ItemPedidoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.sessions.models import Session #manejo de sesiones
#from .forms import pedidos_manuales, pedidos_manuales_cliente
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
# Create your views here.
#
def index(request):
    return render(request, 'compraventa/index.html')



def login_view(request): #el form está directo en el template login.html
    if 'next' in request.GET:
        #si en la url está la palabra "next", generada al redirigir desde @login_required, enviar mensaje.
        messages.add_message(request, messages.INFO, 'Debe ingresar para acceder a las funcionalidades.')

    if request.method == "POST":
        username = request.POST["usuario"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            
            login(request, user)
            return HttpResponseRedirect(reverse("hola"))
        else:
            context= ["Credenciales Inválidas"]#si no lo hago como lista, itera por cada caracter del string.
            return render(request, "compraventa/login.html", {"messages": context})

    return render(request, "compraventa/login.html") #view del login

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        print(form)
        if form.is_valid():
            
            user = form.save() #guardar formulario
            grupo = Group.objects.get(name='usuario_cliente') #buscar el grupo
            user.groups.add(grupo)  #asignarlo al usuario
            cliente = Cliente(
                user=user,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                rut=form.cleaned_data['rut'],
                telefono_movil=form.cleaned_data['telefono_movil'],
                telefono_fijo=form.cleaned_data['telefono_fijo'],
                notas= form.cleaned_data['notas'],
                #direcciones=form.cleaned_data['direcciones']
            )
            cliente.save()
            messages.success(request, 'Usuario ingresado exitosamente')
            return redirect('login')
    else:
        form = RegistrarUsuarioForm()
        
    return render(request, "compraventa/registro.html", {'form': form})
def hola(request):
    return render(request,"compraventa/hola.html")

def logout_view(request):
    
    logout(request)
    return render(request, "compraventa/logout.html")



class ProductoListView(ListView):
    model = Producto
    paginate_by = 10
 
    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        return context #lista de contextos final   
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #este método utiliza condiciones lógicas sobre el contenido del POST, para decidir qué se hace con la información.
        

        if not request.session.session_key: #asegurarse de que exista sesión y que tenga asignada un session_key (en SOF decía que podía darse el caso)
            request.session.save()
        session_id = request.session.session_key #obtiene session_key, para asignarlo luego a pk de Pedido
      
        user_id = request.user.id #id de usuario logueado
       
        cliente_id = Cliente.objects.get(user_id=user_id) #obtiene el cliente a partir del usuario, recordar que cliente tiene
        #relación 1 a 1 con un usuario.

        pedido = Pedido.objects.filter(id_pedido=session_id).exists() #devuelve True si existe un pedido con un id_pedido = session_key,
        # el que podría existir si es que ya se generó instancias de ItemPedido al haber agregado itemes al carrito

        if not pedido: #si no hay un pedido
            Pedido.objects.create(id_pedido=session_id, cliente_solicitante=cliente_id) #crea uno
        pedido = Pedido.objects.get(cliente_solicitante=cliente_id, id_pedido=session_id) #finalmente, asigna un objeto Pedido a la variable pedido

        if 'cantidad' in request.POST: #si en el POST viene un campo 'cantidad':
         
            cantidad = request.POST['cantidad'] #obtiene la cantidad desde el POST
            id_producto = request.POST['id_producto'] #obtiene el id_producto desde el POST
            producto = Producto.objects.get(id_producto=id_producto) #obtiene instancia del producto agregado y la asigna a 'producto'
            item_pedido = ItemPedido.objects.create(cantidad=cantidad, pedido=pedido, producto=producto) #lo mismo con item_pedido
   
            item_pedido.save() #y guarda   
    
        item_pedido.save() #guarda
        return redirect('productos') #redirige al listview, reflejándose el cambio de inmediato.
 









"""


def pedido_manual(request):
    form = pedidos_manuales()

    if request.method == "POST":
        print(request)
        form = pedidos_manuales(request.POST)

        if form.is_valid():
            print(form)
            pedido = Pedido()
            pedido.cliente_solicitante = form.cleaned_data['cliente_solicitante']
            pedido.producto = form.cleaned_data['productos']
            #pedido.numero_transaccion = #pull highest number in database + 1
            #pedido.subtotal = sum(producto.precio for producto in form.cleaned_data['productos'])
            #-- estimar numero de orden
            #--falla si está vacío    
            if Pedido.objects.exists():
                ultimo_pedido = Pedido.objects.latest('numero_transaccion')
                pedido.numero_transaccion = ultimo_pedido.numero_transaccion + 1
            else:
                pedido.numero_transaccion = 1
            pedido.subtotal = pedido.productos.precio
            pedido.fecha_pedido = datetime.datetime.now()
            pedido.save()
            messages.success(request, 'Pedido ingresado exitosamente')
        else:
            print("Datos invalidos")
        return redirect('pedido_manual')
    context = {
        'form': form
    }
    return render(request, 'compraventa/pedidos.html', context=context)

def pedido_manual_cliente(request):
    form = pedidos_manuales_cliente()
    if request.method == "POST":
        form = pedidos_manuales_cliente(request.POST)
        if form.is_valid():
            pedido = Pedido()
            try:
                cliente = Cliente.objects.get(user=request.user)
                pedido.cliente_solicitante = cliente
            except Cliente.DoesNotExist:
                raise ValueError("No se encuentra el cliente de origen")

            productos = form.cleaned_data['productos']
            selected_productos = list(productos) 
            pedido.productos.set(selected_productos)

            #for producto in productos:
            #    print(producto)
            #    pedido.productos.set(producto)
            #pedido.productos = form.cleaned_data['productos']
            #aparentemnete tendremos que hacer producto.set()
            pedido.tiene_despacho = form.cleaned_data['tiene_despacho']
            pedido.subtotal = pedido.productos.precio
            pedido.fecha_pedido = datetime.datetime.now()
            pedido.save()
            messages.success(request, 'Pedido ingresado exitosamente')
        else:
            print("Datos invalidos")
        return redirect('pedido_manual_cliente')
    context = {
        'form': form
    }
    return render(request, 'compraventa/pedidos externos.html', context=context)
"""



     