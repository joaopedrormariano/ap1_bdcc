from rest_framework import serializers
from produtos.models import Produto
from .models import Pedido, ItemPedido

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = ItemPedido
        fields = [
            'id', 'produto', 'produto_nome',
            'quantidade', 'preco_unitario', 'subtotal',
        ]
        extra_kwargs = {'preco_unitario': {'required': False}}

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    quantidade_itens = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente_nome', 'cliente_email', 'status',
            'itens', 'quantidade_itens', 'total',
            'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

class AdicionarItemSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    quantidade = serializers.IntegerField(min_value=1, default=1)
