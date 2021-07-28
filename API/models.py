from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


def profile_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.username, filename)


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    def __str__(self):
        return self.username

    channel_type_choices = [
        ('fashion/beauty', '패션/뷰티'),
        ('food', '푸드'),
        ('daily', '일상'),
        ('asmr', 'ASMR'),
        ('game', '게임'),
        ('animal', '동물'),
        ('movie', '영화'),
        ('music/dance', '음악/춤'),
        ('sports', '스포츠'),
        ('tech', '테크'),
        ('news', '뉴스'),
        ('knowledge', '지식/정보'),
        ('fun', 'FUN'),
        ('etc', '기타'),
    ]

    account_bank_choice = [
        ('SH', '신한은행'),
        ('KA', '카카오뱅크'),
        ('NH', '농협'),
        ('KB', '국민은행'),
        ('WR', '우리은행'),
        ('IBK', '기업은행'),
        ('HN', '하나은행'),
    ]

    nickname = models.CharField(unique=True, null=False, blank=False)
    profile_img = ProcessedImageField(upload_to=profile_directory_path,
                                      processors=[Thumbnail(300, 300)],
                                      format='JPEG',
                                      options={'quality': 80})
    is_creator = models.BooleanField(null=False, blank=True, default=False)
    channel_url = models.URLField(null=False, blank=True, unique=True)
    channel_type = models.CharField(null=False, blank=True, choices=channel_type_choices)
    channel_intro = models.CharField(null=False, blank=True, max_length=20)
    account_bank = models.CharField(null=False, blank=True, choices=account_bank_choice)
    account_name = models.CharField(null=False, blank=True)
    account_num = models.CharField(null=False, blank=True)

    REQUIRED_FIELDS = [nickname]


class Request(TimeStampModel):

    def __str__(self):
        return self.request_name

    request_status_choice = [
        ('request', '요청중'),
        ('quit', '취소'),
        ('proceed', '진행중'),
        ('refuse', '거절'),
        ('done', '완료'),
    ]

    users = models.ManyToManyField('User', related_name='users')
    request_name = models.CharField(null=False, blank=False)
    request_content = models.CharField(null=False, blank=False)
    request_reward = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(100)])
    request_status = models.CharField(null=False, blank=False, choices=request_status_choice)
    request_duedate = models.DateTimeField(null=False, blank=False)
    creator_YN = models.BooleanField(null=False, blank=False, default=False)


class Product(TimeStampModel):

    def __str__(self):
        return self.request_id.request_name

    request_id = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='request')
    request_url = models.URLField(null=False, blank=False)