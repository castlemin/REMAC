from django.urls import path
from .views import get_bank_choice, get_channel_category_choice, ProfileImageView, MainpageView,\
    CustomUserViewSet, CreateRequestView, UserDetailView, UserRequestView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', CustomUserViewSet)

urlpatterns = [
                  path('mainpage/', MainpageView.as_view()),
                  path('profileimage/', ProfileImageView.as_view()),
                  path('bank_choice/', get_bank_choice),
                  path('channel_category_choice/', get_channel_category_choice),
                  path('create_request/', CreateRequestView.as_view()),
                  path('user_detail/', UserDetailView.as_view()),
                  path('user_request/', UserRequestView.as_view()),
              ] + router.urls
