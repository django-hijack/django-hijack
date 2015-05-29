from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import RequestContext

from hijack.helpers import get_can_hijack_function


register = template.Library()


@register.filter
def hijackNotification(request):
    ans = ''
    if getattr(settings, 'HIJACK_NOTIFY_ADMIN',
               True) and request and request.session.get('is_hijacked_user',
                                                         False):
        ans = render_to_string('hijack/notifications.html', {},
                               context_instance=RequestContext(request))
    return mark_safe(ans)


@register.filter
def can_hijack(hijacker, hijacked):
    can_hijack_func = get_can_hijack_function()

    return can_hijack_func(hijacker, hijacked)
