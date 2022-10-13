import django

__version__ = "4.0.0"  # pragma: no cover

if django.VERSION < (3, 2):
    default_app_config = "hijack.apps.HijackConfig"
