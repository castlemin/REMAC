import os
from .base import *
from config.settings import prod_db

DEBUG = False  # 수정
WSGI_APPLICATION = 'config.wsgi.prod.application'  # 수정
INSTALLED_APPS += []

DATABASES = prod_db.DATABASES
SECRET_KEY = prod_db.SECRET
ALLOWED_HOSTS = prod_db.ALLOWED_HOSTS
