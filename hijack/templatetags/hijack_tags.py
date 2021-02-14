import warnings

from django import template
from django.utils.module_loading import import_string

from hijack import settings as hijack_settings

register = template.Library()


@register.filter
def hijackNotification(request):
    warnings.warn('Deprecated favoring "hijack_notification".', DeprecationWarning)
    return ""


@register.simple_tag(takes_context=True)
def hijack_notification(context):
    warnings.warn(
        'Deprecated favoring "HijackRemoteUserMiddleware".', DeprecationWarning
    )
    return ""


@register.filter
def can_hijack(hijacker, hijacked):
    check_authorization = import_string(hijack_settings.HIJACK_AUTHORIZATION_CHECK)
    return check_authorization(hijacker, hijacked)


@register.filter
def is_hijacked(request):
    return request.session.get("is_hijacked_user", False)


try:
    from django_jinja import library

    @library.filter
    def jinja_hijack_notification(request, template_name=None):
        warnings.warn(
            'Deprecated favoring "HijackRemoteUserMiddleware".', DeprecationWarning
        )
        return ""


except ImportError:
    pass
