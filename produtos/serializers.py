from rest_framework import serializers
from .models import Produto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'data_criacao']


class ProdutoSerializer(serializers.ModelSerializer):
    # Mostra o nome da categoria na leitura (leitura amigável)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'preco', 'imagem',
            'categoria', 'categoria_nome', 'data_criacao'
        ]