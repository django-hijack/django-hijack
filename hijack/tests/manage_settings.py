from .test_settings import *  # noqa: F401, F403

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test', }
}

LOCALE_PATHS = (
    'hijack/locale/',
)
