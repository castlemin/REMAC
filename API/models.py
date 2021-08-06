from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


def profile_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.username, filename)


bank_choice = [
    ('SH', '신한은행'),
    ('KA', '카카오뱅크'),
    ('NH', '농협'),
    ('KB', '국민은행'),
    ('WR', '우리은행'),
    ('IBK', '기업은행'),
    ('HN', '하나은행'),
]


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

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

    nickname = models.CharField(unique=True, null=False, blank=False, max_length=12)
    profile_image = ProcessedImageField(upload_to=profile_directory_path,
                                        processors=[Thumbnail(300, 300)],
                                        format='JPEG',
                                        options={'quality': 80},
                                        default='default/default_img.jpg')
    is_creator = models.BooleanField(null=False, blank=True, default=False)
    channel_url = models.URLField(null=False, blank=True)
    channel_category = models.CharField(null=False, blank=True, max_length=20, choices=channel_category_choices)
    channel_intro = models.CharField(null=False, blank=True, max_length=20)
    bank = models.CharField(null=False, blank=True, max_length=20, choices=bank_choice)
    depositor = models.CharField(null=False, blank=True, max_length=10)
    account = models.CharField(null=False, blank=True, max_length=20)

    REQUIRED_FIELDS = ['nickname']


class Request(TimeStampModel):

    def __str__(self):
        return self.request_title

    request_status_choice = [
        ('request', '요청중'),
        ('quit', '취소'),
        ('proceed', '제작중'),
        ('refuse', '반려'),
        ('done', '완료'),
    ]

    users = models.ManyToManyField('CustomUser', related_name='requests')
    request_title = models.CharField(null=False, blank=False, max_length=20)
    request_content = models.CharField(null=False, blank=False, max_length=255)
    request_reward = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(100)])
    request_status = models.CharField(null=False, blank=False, max_length=20, choices=request_status_choice,
                                      default='request')
    request_duedate = models.DateField(null=False, blank=False)
    creator_YN = models.BooleanField(null=False, blank=False, default=False)
    refund_bank = models.CharField(null=False, blank=True, max_length=20, choices=bank_choice)
    refund_depositor = models.CharField(null=False, blank=True, max_length=10)
    refund_account = models.CharField(null=False, blank=True, max_length=20)


class Product(TimeStampModel):

    def __str__(self):
        return self.request_id.request_title

    request_id = models.OneToOneField('Request', on_delete=models.CASCADE, related_name='product')
    product_url = models.URLField(null=False, blank=False)
