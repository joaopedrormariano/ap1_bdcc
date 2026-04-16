from rest_framework import viewsets
from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria').all()
    serializer_class = ProdutoSerializer