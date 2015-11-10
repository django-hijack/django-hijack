from .test_settings import *

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test', }
}

LOCALE_PATHS = (
    'hijack/locale/',
)
