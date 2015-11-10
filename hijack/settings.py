# -*- coding: utf-8 -*-
from django.conf import settings


SHOW_HIJACKUSER_IN_ADMIN = getattr(settings, 'SHOW_HIJACKUSER_IN_ADMIN', True)
SHOW_SESSIONS_IN_ADMIN = getattr(settings, 'SHOW_SESSIONS_IN_ADMIN', False)
HIJACK_NOTIFY_ADMIN = getattr(settings, "HIJACK_NOTIFY_ADMIN", True)

ALLOWED_HIJACKING_USER_ATTRIBUTES = getattr(settings, 'ALLOWED_HIJACKING_USER_ATTRIBUTES', ())

ALLOW_STAFF_TO_HIJACKUSER = getattr(settings, "ALLOW_STAFF_TO_HIJACKUSER", False)
ALLOW_STAFF_TO_HIJACK_STAFF_USER = getattr(settings, "ALLOW_STAFF_TO_HIJACK_STAFF_USER", False)

HIJACK_LOGIN_REDIRECT_URL = getattr(settings, 'HIJACK_LOGIN_REDIRECT_URL',
                                    getattr(settings, 'LOGIN_REDIRECT_URL', '/'))
REVERSE_HIJACK_LOGIN_REDIRECT_URL = getattr(settings, 'REVERSE_HIJACK_LOGIN_REDIRECT_URL',
                                            getattr(settings, 'LOGIN_REDIRECT_URL', '/'))

CUSTOM_HIJACK_HANDLER = getattr(settings, 'CUSTOM_HIJACK_HANDLER', None)
