# coding: utf-8
"""
Django settings for pinbot_xywz project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from __future__ import unicode_literals
import os
import sys
import six

if six.PY2 and sys.getdefaultencoding() == 'ascii':
    # reload(sys)
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf-8')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

MEDIA_URL = '/media/'

STATIC_ROOT1 = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
if not os.path.exists(STATIC_ROOT1):
    os.mkdir(STATIC_ROOT1)
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '4(bzt*4h3_0q&b3n^e2$bf564x3@6g0b^78197no@(@auln-1q'

SECRET_KEY = '$^0#lv$kycl5!kdfDkdf@@@@+//>Qlkdfdf***-!'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '192.168.3.103',
    '192.168.2.188',
    '0.0.0.0',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'apps.ttxs_auth',
    'apps.park'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'ttxs_yw.urls'

# 默认登录使用的backend
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # 默认backend
)
USERNAME_FIELD = ['username', 'email']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# logging setting
# LOG_ROOT = os.path.join(os.path.dirname(__file__), '../../logs')
###########################################################
#                       日志系统配置
###########################################################
LOG_SQL_IN_FILE = False  # 是否将debug级别的SQL语句输出写入日志文件
SQL_LOG_LEVEL = 'INFO'  # 该设置决定是否输出SQL语句, django框架的SQL语句仅在DEBUG级才能输出. 默认仅输出到console
DJANGO_LOG_LEVEL = 'DEBUG'  # 该设置决定django框架自身的日志输出
BUSINESS_LOG_LEVEL = 'INFO'  # 业务模块日志级别

# 类似于nat_server的log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 默认配置中的所有logger 都将禁用
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'},
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "ttxs_yw.log"),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "ttxs_yw.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', ] if LOG_SQL_IN_FILE else ['console'],
            'level': SQL_LOG_LEVEL,
            'propagate': False,
        },
        'ttxs-yw': {
            'handlers': ['console', 'default', 'error'],
            'level': BUSINESS_LOG_LEVEL,
        },
    }
}

# swagger setting
SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
    'JSON_EDITOR': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'USE_SESSION_AUTH': True,
    'SHOW_REQUEST_HEADERS': True,
}

TIME_ZONE = 'Asia/Shanghai'
# LANGUAGE_CODE = 'zh-cn'

USE_I18N = True
USE_TZ = False

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # drf 默认auth方法
        'rest_framework.authentication.BasicAuthentication',  # DRF中最基本的认证
        'rest_framework.authentication.TokenAuthentication',    # 这里为drf默认的token在headers中认证
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',   # JWT 默认认证
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 权限模块, 登录后有权限
    ),
    # 分页设置
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.Pagination',
    'PAGE_SIZE': 10,
    'MAX_PAGE_SIZE': 10,

    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    # 时间格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M:%S', ],

    # 自定义错误
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # 自定义渲染器, 数据返回格式
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # rest_framework postman 浏览器模式
    )

}


import datetime

JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': True,  # 是否设置过期,默认设置为true
    'JWT_ALLOW_REFRESH': True,  # JWT 允许刷新操作
    # 5mins + 7days的默认设置
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 客户端首先调用obtain_jwt_token进行登录操作，之后必须每隔小于5分钟就刷新一次token，才能保证不掉线
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 即使一直保持在线，上限也只有7天，7天过后必须重新登录
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:3030',
    '127.0.0.1',
)
CORS_ORIGIN_REGEX_WHITELIST = (
    'localhost:3030',
    '127.0.0.1',
)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'admin',
        'PORT': 3306,
        'NAME': 'park_manage',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },
}

"""
create database park_manage default character set utf8;
docker run --name my_mysql -e MYSQL_ROOT_PASSWORD=admin -d  -it -p 3306:3306 mysql
python manage.py makemigrations
python manage.py migrate
python manage.py create_postions
python manage.py createsuperuser
    - admin01 / admin01
    - admin02 / admin02
    - admin-3 / admin03

# vue 
cd park_vue
npm install
npm audit fix --force

"""