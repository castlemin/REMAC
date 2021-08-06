from rest_framework.viewsets import ModelViewSet
from API.models import Request, Product
from .serializers import DialogSerializer, ProductSerializer


class DialogViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = DialogSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
