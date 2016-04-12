# -*- coding: utf-8 -*-
from django.conf import settings as django_settings

SETTINGS = (
    {
        'name': 'HIJACK_DISPLAY_WARNING',
        'default': True,
        'legacy_name': 'HIJACK_NOTIFY_ADMIN',
    },
    {
        'name': 'HIJACK_URL_ALLOWED_ATTRIBUTES',
        'default': ('user_id', 'email', 'username'),
        'legacy_name': 'ALLOWED_HIJACKING_USER_ATTRIBUTES',
    },
    {
        'name': 'HIJACK_AUTHORIZE_STAFF',
        'default': False,
        'legacy_name': 'ALLOW_STAFF_TO_HIJACKUSER',
    },
    {
        'name': 'HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF',
        'default': False,
        'legacy_name': 'ALLOW_STAFF_TO_HIJACK_STAFF_USER',
    },
    {
        'name': 'HIJACK_ALLOW_GET_REQUESTS',
        'default': False,
        'legacy_name': None,
    },
    {
        'name': 'HIJACK_LOGIN_REDIRECT_URL',
        'default': getattr(django_settings, 'LOGIN_REDIRECT_URL', '/'),
        'legacy_name': None,
    },
    {
        'name': 'HIJACK_LOGOUT_REDIRECT_URL',
        'default': getattr(django_settings, 'LOGIN_REDIRECT_URL', '/'),
        'legacy_name': 'REVERSE_HIJACK_LOGIN_REDIRECT_URL',
    },
    {
        'name': 'HIJACK_AUTHORIZATION_CHECK',
        'default': 'hijack.helpers.is_authorized_default',
        'legacy_name': 'CUSTOM_HIJACK_HANDLER',
    },
    {
        'name': 'HIJACK_DECORATOR',
        'default': 'django.contrib.admin.views.decorators.staff_member_required',
        'legacy_name': None,
    },
    {
        'name': 'HIJACK_USE_BOOTSTRAP',
        'default': False,
        'legacy_name': None,
    },
)

for setting in SETTINGS:
    if setting['legacy_name']:
        default = getattr(django_settings, setting['legacy_name'], setting['default'])
    else:
        default = setting['default']
    value = getattr(django_settings, setting['name'], default)
    globals()[setting['name']] = value
