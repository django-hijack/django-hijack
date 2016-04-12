# -*- encoding: utf-8 -*-
from compat import import_string
from django.views.decorators.http import require_http_methods

from hijack import settings as hijack_settings


def hijack_decorator(fn):
    """
    Apply customizable decorator to sensitive methods. Default: staff_member_required
    """
    decorator = import_string(hijack_settings.HIJACK_DECORATOR)
    return decorator(fn)


def hijack_require_http_methods(fn):
    """
    Wrapper for "require_http_methods" decorator. POST required by default, GET can optionally be allowed
    """
    required_methods = ['POST']
    if hijack_settings.HIJACK_ALLOW_GET_REQUESTS:
        required_methods.append('GET')
    return require_http_methods(required_methods)(fn)
