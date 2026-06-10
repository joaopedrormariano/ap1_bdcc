from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
]
