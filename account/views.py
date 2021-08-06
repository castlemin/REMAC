from django.contrib import auth
from django.http import Http404
from API.models import CustomUser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AfterRegisterSerialiezer, RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class AfterRegisterView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AfterRegisterSerialiezer

    def get_object(self):
        try:
            instance = self.queryset.get(pk=self.request.user.pk)
            return instance
        except CustomUser.DoesNotExist:
            raise Http404

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"로그아웃을 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
