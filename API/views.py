from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import CustomUser, Request
from .serializers import CustomUserSerializer, CreateRequestSerializer, MainpageSerializer, \
    ProfileImageSerializer, UserDetailSerializer, UserRequestSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def get_channel_category_choice(request):
    data = [
        # ('fashion', '패션'),
        # ('beauty', '뷰티'),
        ('food', '푸드'),
        # ('daily', '일상'),
        # ('asmr', 'ASMR'),
        ('game', '게임'),
        # ('animal', '동물'),
        # ('movie', '영화'),
        ('music', '음악'),
        # ('dance', '춤'),
        # ('sports', '스포츠'),
        # ('tech', '테크'),
        ('knowledge', '학습'),
        # ('fun', 'FUN'),
        # ('etc', '기타'),
        ('review', '리뷰')
    ]
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_bank_choice(request):
    data = [
        ('SH', '신한은행'),
        ('KA', '카카오뱅크'),
        ('NH', '농협'),
        ('KB', '국민은행'),
        ('WR', '우리은행'),
        ('IBK', '기업은행'),
        ('HN', '하나은행'),
    ]
    return Response(data)

# NOT USED
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CreateRequestView(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = CreateRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'201 Created': '요청이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MainpageView(ListAPIView):
    queryset = CustomUser.objects.filter(is_creator=True)
    serializer_class = MainpageSerializer
    permission_classes = [AllowAny]


class ProfileImageView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileImageSerializer

    def get_object(self):
        try:
            instance = self.queryset.get(pk=self.request.user.pk)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404


class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        try:
            instance = self.queryset.get(pk=self.request.user.pk)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404

# NOT USED
class UserRequestView(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = UserRequestSerializer

    def get_object(self):
        try:
            instance = self.queryset.get(self.request.user in User)
            for i in instance:
                for user in i["users"]:
                    if user["id"] == self.request.user.pk:
                        i["users"].remove(user)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404
