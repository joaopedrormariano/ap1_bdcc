from rest_framework import serializers
from .models import Categoria, Produto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'slug', 'descricao']
        read_only_fields = ['slug']

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    imagem_url = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'preco', 'estoque', 'ativo',
            'categoria', 'categoria_nome',
            'imagem', 'imagem_url', 'atributos',
            'data_criacao', 'data_atualizacao',
        ]
        read_only_fields = ['data_criacao', 'data_atualizacao']

    def get_imagem_url(self, obj):
        if not obj.imagem:
            return None
        url = obj.imagem.url
        request = self.context.get('request')
        if request is not None and url.startswith('/'):
            return request.build_absolute_uri(url)
        return url
