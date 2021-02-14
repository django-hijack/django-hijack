from django import template
from django.utils.module_loading import import_string

from hijack.conf import settings

register = template.Library()


@register.filter
def can_hijack(hijacker, hijacked):
    """
    Test if a user can hijack another user.

    Usage:

        {% if request.user|can_hijack:another_user %}
          {# The currently authenticated user can hijack the user "another_user". #}
        {% endif %}

    """
    func = import_string(settings.HIJACK_PERMISSION_CHECK)
    return func(hijacker=hijacker, hijacked=hijacked)
