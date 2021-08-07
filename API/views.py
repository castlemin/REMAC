from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import CustomUser, Request
from .serializers import CustomUserSerializer, CreateRequestSerializer, MainpageSerializer, \
    ProfileImageSerializer, UserDetailSerializer, UserRequestSerializer

User = get_user_model()


def index(request):
    return render(request, 'REMAC/templates/index.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def get_channel_category_choice(request):
    data = [
        ('fashion', '패션'),
        ('beauty', '뷰티'),
        ('food', '푸드'),
        ('daily', '일상'),
        ('asmr', 'ASMR'),
        ('game', '게임'),
        ('animal', '동물'),
        ('movie', '영화'),
        ('music', '음악'),
        ('dance', '춤'),
        ('sports', '스포츠'),
        ('tech', '테크'),
        ('knowledge', '지식'),
        ('fun', 'FUN'),
        ('etc', '기타'),
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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CreateRequestView(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = CreateRequestSerializer


class MainpageView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MainpageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['channel_category', 'is_creator']


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


class UserRequestView(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = UserRequestSerializer

    def get_object(self):
        try:
            instance = self.queryset.get(self.request.user in users)
            for i in instance:
                for user in i["users"]:
                    if user["id"] == self.request.user.pk:
                        i["users"].remove(user)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404
