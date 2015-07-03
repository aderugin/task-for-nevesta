# -*- coding: utf-8 -*-
import os
from . import *


DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'test_task_gallery'),
        'USER': os.environ.get('DB_USR', ''),
        'PASSWORD': os.environ.get('DB_PSWD', ''),
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST_CHARSET': 'utf8',
    }
}
