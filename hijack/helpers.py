# -*- coding: utf-8 -*-
import contextlib
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login, load_backend, BACKEND_SESSION_KEY
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import is_safe_url

from compat import get_user_model, import_string
from compat import resolve_url

from hijack import settings as hijack_settings
from hijack.signals import hijack_started, hijack_ended


@contextlib.contextmanager
def no_update_last_login():
    """
    Disconnect any signals to update_last_login() for the scope of the context
    manager, then restore.
    """
    kw = {'receiver': update_last_login}
    kw_id = {'receiver': update_last_login, 'dispatch_uid': 'update_last_login'}

    was_connected = user_logged_in.disconnect(**kw)
    was_connected_id = not was_connected and user_logged_in.disconnect(**kw_id)
    yield
    # Restore signal if needed
    if was_connected:
        user_logged_in.connect(**kw)
    elif was_connected_id:
        user_logged_in.connect(**kw_id)


def get_used_backend(request):
    backend_str = request.session[BACKEND_SESSION_KEY]
    backend = load_backend(backend_str)
    return backend


def release_hijack(request):
    hijack_history = request.session.get('hijack_history', False)

    if not hijack_history:
        raise PermissionDenied

    hijacker = None
    hijacked = None
    if hijack_history:
        hijacked = request.user
        user_pk = hijack_history.pop()
        hijacker = get_object_or_404(get_user_model(), pk=user_pk)
        backend = get_used_backend(request)
        hijacker.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        with no_update_last_login():
            login(request, hijacker)
    if hijack_history:
        request.session['hijack_history'] = hijack_history
        request.session['is_hijacked_user'] = True
        request.session['display_hijack_warning'] = True
    else:
        request.session.pop('hijack_history', None)
        request.session.pop('is_hijacked_user', None)
        request.session.pop('display_hijack_warning', None)
    request.session.modified = True
    hijack_ended.send(
            sender=None, request=request,
            hijacker=hijacker, hijacked=hijacked,
            # send IDs for backward compatibility
            hijacker_id=hijacker.pk, hijacked_id=hijacked.pk)
    return redirect_to_next(request, default_url=hijack_settings.HIJACK_LOGOUT_REDIRECT_URL)


def is_authorized_default(hijacker, hijacked):
    """Checks if the user has the correct permission to Hijack another user.

    By default only superusers are allowed to hijack.

    An exception is made to allow staff members to hijack when
    HIJACK_AUTHORIZE_STAFF is enabled in the Django settings.

    By default it prevents staff users from hijacking other staff users.
    This can be disabled by enabling the HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF
    setting in the Django settings.

    Staff users can never hijack superusers.
    """

    if hijacker.is_superuser:
        return True

    if hijacked.is_superuser:
        return False

    if hijacker.is_staff and hijack_settings.HIJACK_AUTHORIZE_STAFF:
        if hijacked.is_staff and not hijack_settings.HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF:
            return False
        return True

    return False


def is_authorized(hijack, hijacked):
    '''
    Evaluates the authorization check specified in settings
    '''
    authorization_check = import_string(hijack_settings.HIJACK_AUTHORIZATION_CHECK)
    return authorization_check(hijack, hijacked)


def check_hijack_authorization(request, user):
    if not is_authorized(request.user, user):
        raise PermissionDenied


def login_user(request, hijacked):
    ''' hijack mechanism '''
    hijacker = request.user
    hijack_history = [request.user._meta.pk.value_to_string(hijacker)]
    if request.session.get('hijack_history'):
        hijack_history = request.session['hijack_history'] + hijack_history

    check_hijack_authorization(request, hijacked)

    backend = get_used_backend(request)
    hijacked.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)

    with no_update_last_login():
        # Actually log user in
        login(request, hijacked)

    hijack_started.send(
            sender=None, request=request,
            hijacker=hijacker, hijacked=hijacked,
            # send IDs for backward compatibility
            hijacker_id=hijacker.pk, hijacked_id=hijacked.pk)
    request.session['hijack_history'] = hijack_history
    request.session['is_hijacked_user'] = True
    request.session['display_hijack_warning'] = True
    request.session.modified = True
    return redirect_to_next(request, default_url=hijack_settings.HIJACK_LOGIN_REDIRECT_URL)


def redirect_to_next(request, default_url=hijack_settings.HIJACK_LOGIN_REDIRECT_URL):
    redirect_to = request.GET.get('next', '')
    if not is_safe_url(redirect_to):
        redirect_to = default_url
    return HttpResponseRedirect(resolve_url(redirect_to))
