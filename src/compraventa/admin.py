from django.contrib import admin
from .models import Pedido, Producto, Proveedor, Cliente, Sucursal, Categoria

#imports para inline de CLiente
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.
#admin.site.register(Pedido) deberían poder modificar los pedidos?
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Sucursal)
admin.site.register(Categoria)

#entonces, se crea un modelo 'inline', que permite que se puedan editar campos en el admin
#copio y pego lo indicado en la documentación, adaptado por supuesto.
#https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#extending-the-existing-user-model


# Define an inline admin descriptor for Cliente model
# which acts a bit like a singleton (un singleton es una clase que sólo permite UNA instancia)
class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = "cliente"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ClienteInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
