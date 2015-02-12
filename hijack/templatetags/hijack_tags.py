from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import RequestContext

register = template.Library()

@register.filter
def hijackNotification(request):
    ans = ''
    if getattr(settings, 'HIJACK_NOTIFY_ADMIN', True) and request.session.get('is_hijacked_user', False):
        ans = render_to_string('hijack/notifications.html', {}, context_instance=RequestContext(request)) 
    return mark_safe(ans) 
    