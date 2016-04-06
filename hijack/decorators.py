# -*- encoding: utf-8 -*-
from compat import import_string

from hijack import settings as hijack_settings


def hijack_decorator(fn):
    decorator = import_string(hijack_settings.HIJACK_DECORATOR)
    return decorator(fn)
