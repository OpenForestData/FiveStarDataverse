"""
Django settings for fivestar project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, '../')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("APPLICATION_SECRET_KEY", 'tw8w$m^s-6qw(uol7^j9qlu+t4@p28ceb+()o&m%sxj62*%o#x')

ALLOWED_HOSTS = ['*', 'agregator.whiteaster.com']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# apps added from libraries
BASE_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # not standard django apps
    # swagger - generating html views fro backend
    'drf_yasg',
    'corsheaders'
]

# local apps in this project
ADDITIONAL_APPS = [
    'api'
]

# installed apps separated to apps from libs, and locally created ones
INSTALLED_APPS = BASE_APPS + ADDITIONAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fivestar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
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
"""
DB Configuration
If Production in evnironment, use production 
db passes
"""

WSGI_APPLICATION = 'fivestar.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Statics
STATIC_URL = '/static-agregator/'

# Media
MEDIA_URL = '/media-agregator/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DATAVERSE_URL = os.environ.get("DATAVERSE_URL")
print(DATAVERSE_URL)

SOLR_COLLECTION_URL = os.environ.get("SOLR_COLLECTION_URL")
print(SOLR_COLLECTION_URL)

BACKEND_CMS_URL = os.environ.get("BACKEND_CMS_URL")
print(BACKEND_CMS_URL)

CORS_ORIGIN_ALLOW_ALL = True

DATASET_DETAILS_MAX_RESULTS_AMOUNT = os.environ.get("DATASET_DETAILS_MAX_RESULTS_AMOUNT")

IMG_PROXY_SALT = os.environ.get('IMG_PROXY_SALT')
IMG_PROXY_KEY = os.environ.get('IMG_PROXY_KEY')

IMG_PROXY_URL = os.environ.get('IMG_PROXY_URL')

IMG_PROXY_AVAILABLE_PARAMS = {
    'resize': [
        'fit', 'fill', 'crop', 'force'
    ],
    'extensions': [
        'jpg', 'png', 'webp'
    ]
}

IMG_PROXY_THUMBNAILS_CREATION_MIME_TYPES = ['image/png', 'image/jpeg', 'image/tiff']

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_BD')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_EXPIRES_TIME_IN_SECONDS = int(os.environ.get('REDIS_EXPIRES_TIME_IN_SECONDS', 1))

METRICS_DATAVERSE_TYPES = ['dataverses', 'datasets', 'files', 'downloads']
