from django import template
from django.utils.module_loading import import_string

from hijack.conf import settings
from hijack.permissions import can_hijack_user

register = template.Library()


@register.filter()
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


@register.simple_tag(takes_context=True)
def can_hijack_tag(context, hijacker, hijacked):
    """
    Test if the currently authenticated user can hijack another user.

    Usage:

        {% can_hijack_tag hijacker=request.user hijacked=another_user as can_hijack_user %}
        {% if can_hijack_user %}
          {# The currently authenticated user can hijack the user "another_user". #}
        {% endif %}
    """
    return can_hijack_user(hijacker, hijacked, context["request"])
