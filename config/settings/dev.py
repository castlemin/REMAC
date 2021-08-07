import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']  # 모든 호스트 허용
WSGI_APPLICATION = 'config.wsgi.dev.application'  # 수정
INSTALLED_APPS += []

DATABASES = dev_db.DATABASES
SECRET_KEY = dev_db.SECRET
