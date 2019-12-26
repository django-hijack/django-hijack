from django import template
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from hijack import settings as hijack_settings

register = template.Library()


@register.filter
def hijackNotification(request):
    """
    Deprecated. Use the template tag "hijack_notification" below
    """
    return _render_hijack_notification(request)


@register.simple_tag(takes_context=True)
def hijack_notification(context):
    request = context.get('request')
    return _render_hijack_notification(request)


def _render_hijack_notification(request, template_name=None):
    if template_name is None:
        if hijack_settings.HIJACK_USE_BOOTSTRAP:
            template_name = 'hijack/notifications_bootstrap.html'
        else:
            template_name = 'hijack/notifications.html'
    ans = ''
    if request is not None and all([
        hijack_settings.HIJACK_DISPLAY_WARNING,
        request.session.get('is_hijacked_user', False),
        request.session.get('display_hijack_warning', False),
    ]):
        ans = render_to_string(template_name, request=request)
    return mark_safe(ans)


@register.filter
def can_hijack(hijacker, hijacked):
    check_authorization = import_string(
        hijack_settings.HIJACK_AUTHORIZATION_CHECK)
    return check_authorization(hijacker, hijacked)


@register.filter
def is_hijacked(request):
    return request.session.get('is_hijacked_user', False)


try:
    from django_jinja import library

    @library.filter
    def jinja_hijack_notification(request, template_name=None):
        return _render_hijack_notification(request, template_name)

except ImportError:
    pass
