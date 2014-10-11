# CHANGE LOG

2014.10.11
=========================
使用 Redis 作为 django 缓存，并将微信 access_token 缓存迁移到 cache 存储
1. 安装django-redis

    pip install django-redis

[文档地址](http://niwibe.github.io/django-redis/)

2. settings.py 增加

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': '10.0.100.1:6379:1',  # DB 1
            'OPTIONS': {
                'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
                'PASSWORD': '',  # Optional
            }
        }
    }

3. access_token 缓存类设置

    # 默认使用 RedisTokenCache， Redis不可用时，可采用文件缓存
    # TOKEN_CACHE_CLASS = 'changeqr.wechat.conf.RedisTokenCache'
    TOKEN_CACHE_CLASS = 'changeqr.wechat.conf.FileTokenCache'


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
