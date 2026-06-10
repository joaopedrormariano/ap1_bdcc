from decimal import Decimal
from django.db import models
from produtos.models import Produto

class Pedido(models.Model):
    class Status(models.TextChoices):
        ABERTO = 'ABERTO', 'Aberto (carrinho)'
        PAGO = 'PAGO', 'Pago'
        ENVIADO = 'ENVIADO', 'Enviado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    cliente_nome = models.CharField(max_length=200)
    cliente_email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ABERTO,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.itens.all()), Decimal('0.00'))

    @property
    def quantidade_itens(self) -> int:
        return sum(item.quantidade for item in self.itens.all())

    def __str__(self):
        return f'Pedido #{self.pk} - {self.cliente_nome} ({self.status})'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='itens_pedido',
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('pedido', 'produto')
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def save(self, *args, **kwargs):
        if self.preco_unitario is None:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)

    @property
    def subtotal(self) -> Decimal:
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido #{self.pedido_id})'
