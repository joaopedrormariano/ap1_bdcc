from rest_framework import viewsets, filters
from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['preco', 'data_criacao', 'nome']

    def get_queryset(self):
        qs = Produto.objects.select_related('categoria').all()
        params = self.request.query_params

        categoria = params.get('categoria')
        if categoria:
            if categoria.isdigit():
                qs = qs.filter(categoria_id=categoria)
            else:
                qs = qs.filter(categoria__slug=categoria)

        marca = params.get('marca')
        if marca:
            qs = qs.filter(atributos__marca__iexact=marca)

        cor = params.get('cor')
        if cor:
            qs = qs.filter(atributos__cor__iexact=cor)

        ram_min = params.get('ram_min')
        if ram_min and ram_min.isdigit():
            qs = qs.filter(atributos__ram_gb__gte=int(ram_min))

        cpu = params.get('cpu')
        if cpu:
            qs = qs.filter(atributos__especificacoes__cpu__iexact=cpu)

        return qs
