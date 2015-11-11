# -*- coding: utf-8 -*-
from django.core.checks import Error, Warning, register
from django.conf.global_settings import AUTH_USER_MODEL as default_auth_user_model
from django.conf import settings

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

def register_checks():
    for check in [
        check_allowed_hijacking_user_attributes,
        check_show_hijackuser_in_admin_with_custom_user_model,
    ]:
        register(check)