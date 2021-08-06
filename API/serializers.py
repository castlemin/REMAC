from rest_framework import serializers
from .models import CustomUser, Request

bank_choice = [
    ('SH', '신한은행'),
    ('KA', '카카오뱅크'),
    ('NH', '농협'),
    ('KB', '국민은행'),
    ('WR', '우리은행'),
    ('IBK', '기업은행'),
    ('HN', '하나은행'),
]


class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

    def create(self, validated_data):
        instance = super(CreateRequestSerializer, self).create(validated_data)
        instance.users.add(self.context['request'].user)
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}


class MainpageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'is_creator', 'channel_category', 'channel_url', 'channel_intro', 'profile_image']


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image']



class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'profile_image']


class UserRequestSerializer(serializers.ModelSerializer):
    users = CreatorSerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'users', 'request_title', 'created', 'request_status']


class UserDetailSerializer(serializers.ModelSerializer):
    requests = UserRequestSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'nickname', 'profile_image', 'is_creator', 'channel_category',
                  'channel_intro', 'bank', 'depositor', 'account', 'requests']
