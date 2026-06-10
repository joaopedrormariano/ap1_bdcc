from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Categoria, Produto

class ProdutoJSONFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.notebooks = Categoria.objects.create(nome='Notebooks')
        self.perifericos = Categoria.objects.create(nome='Periféricos')
        Produto.objects.create(
            nome='Dell 16GB', categoria=self.notebooks, preco=Decimal('4000'),
            atributos={'marca': 'Dell', 'ram_gb': 16, 'cor': 'preto'},
        )
        Produto.objects.create(
            nome='Lenovo 8GB', categoria=self.notebooks, preco=Decimal('3000'),
            atributos={'marca': 'Lenovo', 'ram_gb': 8, 'cor': 'prata'},
        )
        Produto.objects.create(
            nome='Mouse', categoria=self.perifericos, preco=Decimal('150'),
            atributos={'marca': 'Logitech', 'cor': 'preto'},
        )

    def test_filtro_json_marca(self):
        r = self.client.get('/api/produtos/?marca=Dell')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_filtro_json_ram_min(self):
        r = self.client.get('/api/produtos/?ram_min=16')
        self.assertEqual([p['nome'] for p in r.json()], ['Dell 16GB'])

    def test_filtro_combinado_relacional_e_json(self):
        r = self.client.get('/api/produtos/?categoria=notebooks&cor=preto')
        self.assertEqual([p['nome'] for p in r.json()], ['Dell 16GB'])
