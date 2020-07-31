from .common import *
from fivestar.settings import db_config

DEBUG = True

SSL = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": db_config.DEVELOPMENT_SETTINGS
}

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')