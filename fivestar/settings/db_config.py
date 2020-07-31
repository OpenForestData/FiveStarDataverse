import os

from fivestar.settings.common import PROJECT_DIR

"""
Do not change production env variables
"""

DEVELOPMENT_SETTINGS = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
}

TEST_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'test',
    'USER': 'test',
    'PASSWORD': 'test',
    'HOST': '0.0.0.0',
    'PORT': '5432',
}
PRODUCTION_SETTINGS = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
}
