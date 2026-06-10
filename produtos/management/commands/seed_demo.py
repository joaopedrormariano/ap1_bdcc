from decimal import Decimal
from django.core.management.base import BaseCommand
from produtos.models import Categoria, Produto

class Command(BaseCommand):
    help = 'Cria dados de demonstração (categorias + produtos com atributos JSON).'

    def handle(self, *args, **options):
        notebooks, _ = Categoria.objects.get_or_create(nome='Notebooks')
        perifericos, _ = Categoria.objects.get_or_create(nome='Periféricos')

        dados = [
            {
                'nome': 'Notebook Dell Inspiron 15',
                'categoria': notebooks,
                'preco': Decimal('4299.90'),
                'estoque': 12,
                'atributos': {
                    'marca': 'Dell', 'ram_gb': 16, 'cor': 'preto',
                    'especificacoes': {'cpu': 'i7', 'armazenamento': '512GB SSD'},
                },
            },
            {
                'nome': 'Notebook Lenovo IdeaPad 3',
                'categoria': notebooks,
                'preco': Decimal('3199.00'),
                'estoque': 8,
                'atributos': {
                    'marca': 'Lenovo', 'ram_gb': 8, 'cor': 'prata',
                    'especificacoes': {'cpu': 'i5', 'armazenamento': '256GB SSD'},
                },
            },
            {
                'nome': 'Notebook Dell XPS 13',
                'categoria': notebooks,
                'preco': Decimal('8999.00'),
                'estoque': 4,
                'atributos': {
                    'marca': 'Dell', 'ram_gb': 32, 'cor': 'prata',
                    'especificacoes': {'cpu': 'i7', 'armazenamento': '1TB SSD'},
                },
            },
            {
                'nome': 'Mouse Logitech MX Master 3',
                'categoria': perifericos,
                'preco': Decimal('549.90'),
                'estoque': 30,
                'atributos': {'marca': 'Logitech', 'cor': 'grafite', 'sem_fio': True},
            },
        ]

        for d in dados:
            Produto.objects.get_or_create(nome=d['nome'], defaults=d)

        self.stdout.write(self.style.SUCCESS(
            f'Seed concluído: {Categoria.objects.count()} categorias, '
            f'{Produto.objects.count()} produtos.'
        ))
