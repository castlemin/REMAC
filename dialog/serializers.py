from rest_framework.serializers import ModelSerializer
from API.models import Request, CustomUser, Product


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
        fields = ['id', 'users', 'created', 'updated', 'request_title', 'request_content', 'request_reward',
                  'request_status', 'request_duedate', 'creator_YN', 'product']

