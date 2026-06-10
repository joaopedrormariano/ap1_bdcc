from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pedido, ItemPedido
from .serializers import (
    PedidoSerializer,
    ItemPedidoSerializer,
    AdicionarItemSerializer,
)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.prefetch_related('itens__produto').all()
    serializer_class = PedidoSerializer

    def _resposta_pedido(self, pedido_id, request, http_status=status.HTTP_200_OK):
        pedido = self.get_queryset().get(pk=pedido_id)
        return Response(
            PedidoSerializer(pedido, context={'request': request}).data,
            status=http_status,
        )

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()
        entrada = AdicionarItemSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        produto = entrada.validated_data['produto']
        quantidade = entrada.validated_data['quantidade']

        item, criado = ItemPedido.objects.get_or_create(
            pedido=pedido,
            produto=produto,
            defaults={'quantidade': quantidade, 'preco_unitario': produto.preco},
        )
        if not criado:
            item.quantidade += quantidade
            item.save()

        return self._resposta_pedido(pedido.pk, request)

    @action(detail=True, methods=['post'])
    def remover_item(self, request, pk=None):
        pedido = self.get_object()
        produto_id = request.data.get('produto')
        if not produto_id:
            return Response(
                {'erro': "Informe o campo 'produto' (id)."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        deletados, _ = ItemPedido.objects.filter(
            pedido=pedido, produto_id=produto_id
        ).delete()
        if not deletados:
            return Response(
                {'erro': 'Item não encontrado neste pedido.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self._resposta_pedido(pedido.pk, request)

    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        pedido = self.get_object()
        if not pedido.itens.exists():
            return Response(
                {'erro': 'Carrinho vazio.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if pedido.status != Pedido.Status.ABERTO:
            return Response(
                {'erro': f'Pedido já está {pedido.status}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pedido.status = Pedido.Status.PAGO
        pedido.save()
        return self._resposta_pedido(pedido.pk, request)
