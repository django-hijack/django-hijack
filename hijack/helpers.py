from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import login, get_backends
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from compat import get_user_model
from compat import resolve_url

from hijack.signals import post_superuser_login
from hijack.signals import post_superuser_logout


def release_hijack(request):
    hijack_history = request.session.get('hijack_history', False)

    if not hijack_history:
        raise PermissionDenied

    if hijack_history:
        user_pk = hijack_history.pop()
        user = get_object_or_404(get_user_model(), pk=user_pk)
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__,
                                  backend.__class__.__name__)
        login(request, user)
    if hijack_history:
        request.session['hijack_history'] = hijack_history
        request.session['is_hijacked_user'] = True
    else:
        try:
            del request.session['hijack_history']
            del request.session['is_hijacked_user']
        except KeyError:
            pass
    request.session.modified = True
    redirect_to = request.GET.get('next',
                                  getattr(settings,
                                          'REVERSE_HIJACK_LOGIN_REDIRECT_URL',
                                          getattr(settings,
                                                  'LOGIN_REDIRECT_URL', '/')))
    return HttpResponseRedirect(resolve_url(redirect_to))


def check_hijack_permission(request, user):
    """Checks if the user has the correct permission to Hijack another user.

    By default only superusers are allowed to hijack.

    An exception is made to allow staff members to hijack when
    ALLOW_STAFF_TO_HIJACKUSER is enabled in the Django settings.

    By default it prevents staff users from hijacking other staff users.
    This can be disabled by enabling the ALLOW_STAFF_TO_HIJACK_STAFF_USER
    setting in the Django settings.

    Staff users can never hijack superusers.
    """
    ALLOW_STAFF_TO_HIJACKUSER = getattr(settings, "ALLOW_STAFF_TO_HIJACKUSER",
                                        False)

    ALLOW_STAFF_TO_HIJACK_STAFF_USER = getattr(
        settings, "ALLOW_STAFF_TO_HIJACK_STAFF_USER", False)

    if not request.user.is_superuser:
        if ALLOW_STAFF_TO_HIJACKUSER:
            if not request.user.is_staff or user.is_superuser:
                raise PermissionDenied
            elif user.is_staff and not ALLOW_STAFF_TO_HIJACK_STAFF_USER:
                raise PermissionDenied
        else:
            raise PermissionDenied


def login_user(request, user):
    ''' hijack mechanism '''
    hijack_history = [request.user.pk]
    if request.session.get('hijack_history'):
        hijack_history = request.session['hijack_history'] + hijack_history

    check_hijack_permission(request, user)

    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    post_superuser_login.send(sender=None, user_id=user.pk)
    request.session['is_hijacked_user'] = True
    request.session['hijack_history'] = hijack_history
    request.session.modified = True
    redirect_to = request.GET.get('next',
                                  getattr(settings,
                                          'HIJACK_LOGIN_REDIRECT_URL',
                                          getattr(settings,
                                                  'LOGIN_REDIRECT_URL', '/')))
    return HttpResponseRedirect(resolve_url(redirect_to))


@receiver(user_logged_out)
def logout_user(sender, **kwargs):
    ''' wraps logout signal '''
    user = kwargs['user']
    if hasattr(user, 'id'):
        post_superuser_logout.send(sender=None, user_id=user.pk)
