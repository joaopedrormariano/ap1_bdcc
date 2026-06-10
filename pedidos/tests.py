from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from produtos.models import Produto
from .models import Pedido

class CarrinhoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.p1 = Produto.objects.create(nome='A', preco=Decimal('10.00'))
        self.p2 = Produto.objects.create(nome='B', preco=Decimal('5.00'))
        self.pedido = Pedido.objects.create(cliente_nome='Teste')

    def _add(self, produto_id, qtd):
        return self.client.post(
            f'/api/pedidos/{self.pedido.id}/adicionar_item/',
            {'produto': produto_id, 'quantidade': qtd}, format='json',
        )

    def test_adicionar_item_atualiza_total_na_resposta(self):
        r = self._add(self.p1.id, 2)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['total'], '20.00')
        self.assertEqual(len(r.json()['itens']), 1)

    def test_adicionar_mesmo_produto_soma_quantidade(self):
        self._add(self.p1.id, 1)
        r = self._add(self.p1.id, 3)
        self.assertEqual(r.json()['itens'][0]['quantidade'], 4)

    def test_finalizar_carrinho_vazio_falha(self):
        r = self.client.post(f'/api/pedidos/{self.pedido.id}/finalizar/')
        self.assertEqual(r.status_code, 400)

    def test_finalizar_muda_status_para_pago(self):
        self._add(self.p1.id, 1)
        self._add(self.p2.id, 2)
        r = self.client.post(f'/api/pedidos/{self.pedido.id}/finalizar/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'PAGO')
        self.assertEqual(r.json()['total'], '20.00')
