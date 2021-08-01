from django.conf import settings
from django.urls import exceptions as url_exceptions
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from dj_rest_auth.serializers import LoginSerializer
# from django.contrib.auth import authenticate

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
    from allauth.utils import email_address_exists, get_username_max_length
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

bank_choice = [
    ('SH', '신한은행'),
    ('KA', '카카오뱅크'),
    ('NH', '농협'),
    ('KB', '국민은행'),
    ('WR', '우리은행'),
    ('IBK', '기업은행'),
    ('HN', '하나은행'),
]


# 회원가입 serializer
class CustomRegisterSerializer(RegisterSerializer):
    channel_category_choices = [
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

    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED,
    )
    email = None
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=True)
    is_creator = serializers.BooleanField(required=True)
    channel_url = serializers.URLField(allow_blank=True)
    channel_category = serializers.ChoiceField(allow_blank=True,
                                               choices=channel_category_choices)
    channel_intro = serializers.CharField(allow_blank=True)
    bank = serializers.ChoiceField(allow_blank=True,
                                   choices=bank_choice)
    depositor = serializers.CharField(allow_blank=True)
    account = serializers.CharField(allow_blank=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("입력하신 패스워드가 서로 일치하지 않습니다."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'is_creator': self.validated_data.get('is_creator', ''),
            'channel_url': self.validated_data.get('channel_url', ''),
            'channel_category': self.validated_data.get('channel_category', ''),
            'channel_intro': self.validated_data.get('channel_category', ''),
            'bank': self.validated_data.get('bank', ''),
            'depositor': self.validated_data.get('depositor', ''),
            'account': self.validated_data.get('account', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except ValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


# 로그인 serializer
# class CustomLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=False, allow_blank=True)
#     password = serializers.CharField(style={'input_type': 'password'})
#
#     def authenticate(self, **kwargs):
#         return authenticate(self.context['request'], **kwargs)
#
#     def _validate_username(self, username, password):
#         if username and password:
#             user = self.authenticate(username=username, password=password)
#         else:
#             msg = _('아이디와 비밀번호를 입력해주세요')
#             raise ValidationError(msg)
#
#         return user
#
#
#     @staticmethod
#     def validate_auth_user_status(user):
#         if not user.is_active:
#             msg = _('계정이 비활성화 상태입니다')
#             raise ValidationError(msg)
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#         user = self._validate_username(username,  password)
#
#         if not user:
#             msg = _('아이디와 비밀번호를 확인해주세요')
#             raise ValidationError(msg)
#
#         self.validate_auth_user_status(user)
#
#         attrs['user'] = user
#         return attrs

class CustomLoginSerializer(LoginSerializer):
    email = ''