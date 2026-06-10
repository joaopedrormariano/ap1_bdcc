from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    autocomplete_fields = ('produto',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nome', 'status', 'total', 'criado_em')
    list_filter = ('status',)
    search_fields = ('cliente_nome', 'cliente_email')
    inlines = [ItemPedidoInline]

    @admin.display(description='Total (R$)')
    def total(self, obj):
        return obj.total
