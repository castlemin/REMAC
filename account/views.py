from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from .serializers import CustomRegisterSerializer, CustomLoginSerializer
from dj_rest_auth.views import LogoutView


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomLogoutView(LogoutView):
    pass
