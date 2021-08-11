from rest_framework import serializers
from .models import CustomUser, Request

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

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
    profile_image = Base64ImageField(
        max_length=None, use_url=True,
    )
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
