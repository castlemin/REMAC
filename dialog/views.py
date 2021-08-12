from rest_framework.viewsets import ModelViewSet
from API.models import Request, Product
from .serializers import DialogSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import status



class DialogViewset(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = DialogSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        request = Request.objects.get(id=request.data["request_id"])
        if serializer.is_valid():
            self.perform_create(serializer)
            request.request_status = 'done'
            request.save()
            return Response({"결과물이 생성되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
