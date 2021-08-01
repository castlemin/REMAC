from rest_framework import serializers
from .models import CustomUser, Request, Product


bank_choice = [
    ('SH', '신한은행'),
    ('KA', '카카오뱅크'),
    ('NH', '농협'),
    ('KB', '국민은행'),
    ('WR', '우리은행'),
    ('IBK', '기업은행'),
    ('HN', '하나은행'),
]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}



