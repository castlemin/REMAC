from django.urls import path
from .views import CustomRegisterView, CustomLogoutView #, CustomLoginView
from dj_rest_auth.views import LoginView

urlpatterns = [
    path('registration', CustomRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', CustomLogoutView.as_view()),
]
