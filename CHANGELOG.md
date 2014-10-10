# CHANGE LOG

2014.10.10
=========================
1. 安装 django-rq

    pip install django-rq

[文档地址](https://github.com/ui/django-rq)

2. INSTALLED_APPS添加应用

    INSTALLED_APPS = {
        ***
        'django_rq'
    }

3. 添加URL配置

    url(r'^django-rq/', include('django_rq.urls')),


4. settings.py 增加

    # django-rq相关配置
    RQ_QUEUES = {
        'default': {
            'HOST': '10.0.100.1', # redis服务器地址
            'PORT': 6379,
            'DB': 0,
            'PASSWORD': '',
            'DEFAULT_TIMEOUT': 360,
        }
    }

    # 微信接口配置
    WEIXIN_API = {
        'APP_ID': '',
        'APP_SECRET': '',
        'TOKEN': '',
    }

    # 媒体目录配置
    MEDIA_URL = '/media/'
    # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_ROOT = '/tmp/'

    LOGGING = {
        'version': 1,
        ***
        'handlers': {
            ***
            'task': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'task.log',
                'formatter': 'verbose'
            },
            ***
        },
        'loggers': {
            ***
            'tasks': {
                'handlers': ['console', 'task'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
