from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import login, load_backend, BACKEND_SESSION_KEY
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from compat import get_user_model, import_string
from compat import resolve_url

from hijack.signals import post_superuser_login
from hijack.signals import post_superuser_logout


def get_used_backend(request):
    backend_str = request.session[BACKEND_SESSION_KEY]
    backend = load_backend(backend_str)
    return backend


def release_hijack(request):
    hijack_history = request.session.get('hijack_history', False)

    if not hijack_history:
        raise PermissionDenied

    if hijack_history:
        user_pk = hijack_history.pop()
        user = get_object_or_404(get_user_model(), pk=user_pk)
        backend = get_used_backend(request)
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


def can_hijack(hijacker, hijacked):
    """Checks if the user has the correct permission to Hijack another user.

    By default only superusers are allowed to hijack.

    An exception is made to allow staff members to hijack when
    ALLOW_STAFF_TO_HIJACKUSER is enabled in the Django settings.

    By default it prevents staff users from hijacking other staff users.
    This can be disabled by enabling the ALLOW_STAFF_TO_HIJACK_STAFF_USER
    setting in the Django settings.

    Staff users can never hijack superusers.
    """
    if hijacked.is_superuser and not hijacker.is_superuser:
        return False

    if hijacker.is_superuser:
        return True

    ALLOW_STAFF_TO_HIJACKUSER = getattr(settings, "ALLOW_STAFF_TO_HIJACKUSER",
                                        False)

    ALLOW_STAFF_TO_HIJACK_STAFF_USER = getattr(
        settings, "ALLOW_STAFF_TO_HIJACK_STAFF_USER", False)

    if hijacker.is_staff and ALLOW_STAFF_TO_HIJACKUSER:
        if hijacked.is_staff and not ALLOW_STAFF_TO_HIJACK_STAFF_USER:
            return False
        return True

    return False


def get_can_hijack_function():
    func_dotted_path = getattr(settings, 'CUSTOM_HIJACK_HANDLER', None)
    can_hijack_func = import_string(func_dotted_path) if func_dotted_path else can_hijack

    return can_hijack_func


def check_hijack_permission(request, user):
    can_hijack_func = get_can_hijack_function()

    can_hijack_ret = can_hijack_func(request.user, user)
    if not can_hijack_ret:
        raise PermissionDenied


def login_user(request, user):
    ''' hijack mechanism '''
    hijack_history = [request.user.pk]
    if request.session.get('hijack_history'):
        hijack_history = request.session['hijack_history'] + hijack_history

    check_hijack_permission(request, user)

    backend = get_used_backend(request)
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
