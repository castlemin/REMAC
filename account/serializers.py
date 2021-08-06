from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from API.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


bank_choice = [
    ('SH', '신한은행'),
    ('KA', '카카오뱅크'),
    ('NH', '농협'),
    ('KB', '국민은행'),
    ('WR', '우리은행'),
    ('IBK', '기업은행'),
    ('HN', '하나은행'),
]

UserModel = get_user_model()


# 회원가입 serializer
class RegisterSerializer(serializers.Serializer):
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
        max_length=12,
        min_length=6,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='이미 존재하는 아이디입니다.')])
    password1 = serializers.CharField(
        max_length=12,
        min_length=8,
        required=True,
        write_only=True)
    password2 = serializers.CharField(
        max_length=12,
        min_length=8,
        required=True,
        write_only=True)
    nickname = serializers.CharField(
        max_length=12,
        min_length=2,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='이미 존재하는 닉네임입니다.')])
    is_creator = serializers.BooleanField(required=True)
    channel_url = serializers.URLField(allow_blank=True)
    channel_category = serializers.ChoiceField(allow_blank=True,
                                               choices=channel_category_choices)
    channel_intro = serializers.CharField(max_length=20,
                                          min_length=4,
                                          allow_blank=True)
    bank = serializers.ChoiceField(allow_blank=True,
                                   choices=bank_choice)
    depositor = serializers.CharField(allow_blank=True)
    account = serializers.CharField(allow_blank=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("입력하신 패스워드가 서로 일치하지 않습니다."))
        return data

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            is_creator=validated_data['is_creator'],
            channel_url=validated_data['channel_url'],
            channel_category=validated_data['channel_category'],
            channel_intro=validated_data['channel_intro'],
            bank=validated_data['bank'],
            depositor=validated_data['depositor'],
            account=validated_data['account'],
        )
        user.set_password(validated_data['password1'])
        self.get_tokens_for_user(user)
        user.save()
        return user

# 회원가입 완료 url
class AfterRegisterSerialiezer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname']


# 로그인 serializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


