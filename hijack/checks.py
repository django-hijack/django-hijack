# -*- coding: utf-8 -*-
from django.core.checks import Error, Warning, register
from django.conf.global_settings import AUTH_USER_MODEL as default_auth_user_model
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from compat import import_string
from hijack import settings as hijack_settings

def check_allowed_hijacking_user_attributes(app_configs, **kwargs):
    errors = []
    required_attributes = [
        'user_id',
        'email',
        'username',
    ]
    set_attributes = hijack_settings.ALLOWED_HIJACKING_USER_ATTRIBUTES
    if not any(attribute in set_attributes for attribute in required_attributes):
        errors.append(
            Error(
                'Setting ALLOWED_HIJACKING_USER_ATTRIBUTES needs to be subset of (%s)'
                    % ', '.join(required_attributes),
                hint=None,
                obj=set_attributes,
                id='hijack.E001',
            )
        )
    return errors

def check_show_hijackuser_in_admin_with_custom_user_model(app_configs, **kwargs):
    warnings = []
    if hijack_settings.SHOW_HIJACKUSER_IN_ADMIN \
            and settings.AUTH_USER_MODEL != default_auth_user_model:
        warnings.append(
            Warning(
                'Setting SHOW_HIJACKUSER_IN_ADMIN, which is True by default, '
                'does not work with a custom user model. '
                'Mix HijackUserAdminMixin into your custom UserAdmin or set SHOW_HIJACKUSER_IN_ADMIN to False.',
                hint=None,
                obj=settings.AUTH_USER_MODEL,
                id='hijack.W001',
            )
        )
    return warnings

def check_custom_hijack_handler_importable(app_configs, **kwargs):
    errors = []
    handler = hijack_settings.CUSTOM_HIJACK_HANDLER
    try:
        if handler != staff_member_required:
            import_string(handler)
    except ImportError:
        errors.append(
            Error(
                'Setting CUSTOM_HIJACK_HANDLER cannot be imported',
                hint=None,
                obj=handler,
                id='hijack.E002',
            )
        )
    return errors

def check_hijack_decorator_importable(app_configs, **kwargs):
    errors = []
    decorator = hijack_settings.HIJACK_DECORATOR
    try:
        if decorator != 'django.contrib.admin.views.decorators.staff_member_required':
            import_string(decorator)
    except ImportError:
        errors.append(
            Error(
                'Setting HIJACK_DECORATOR cannot be imported',
                hint=None,
                obj=decorator,
                id='hijack.E003',
            )
        )
    return errors

def register_checks():
    for check in [
        check_allowed_hijacking_user_attributes,
        check_show_hijackuser_in_admin_with_custom_user_model,
        check_custom_hijack_handler_importable,
        check_hijack_decorator_importable,
    ]:
        register(check)