from rest_framework.serializers import ModelSerializer
from API.models import Request, CustomUser, Product
from django.utils import timezone


class DialogUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'profile_image']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'request_id', 'created', 'product_url']


class DialogSerializer(ModelSerializer):
    users = DialogUserSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'users', 'created', 'updated', 'proceed_time', 'request_title', 'request_content', 'request_reward',
                  'request_status', 'request_duedate', 'creator_YN', 'product']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data['request_status'] == 'proceed':
            instance.proceed_time = timezone.now()
            instance.save()
        return instance

# class RequestForProductSerializer(ModelSerializer):
#     class Meta:
#         model = Request
#         fields = ['id']
#
# class ProductRegisterSerializer(ModelSerializer):
#     request_id = RequestForProductSerializer(read_only=True)
#
#     class Meta:
#         model = Product
#         fields = ['request_id', 'product_url']
#
#     def create(self, validated_data):
#         instance = super().create(validated_data)
#         if validated_data["product_url"]:
#             instance.request_id.request_status = 'done'
#             instance.save
#         return instance