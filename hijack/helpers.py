from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import login, get_backends
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from compat import get_user_model

from hijack.signals import post_superuser_login
from hijack.signals import post_superuser_logout


def release_hijack(request):
    if not request.session.get('hijack_history'):
        raise PermissionDenied
    hijack_history = request.session['hijack_history']
    if len(hijack_history):
        user_pk = hijack_history.pop()
        user = get_object_or_404(get_user_model(), pk=user_pk)
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(request, user)
    if len(hijack_history):
        request.session['hijack_history'] = hijack_history
        request.session['is_hijacked_user'] = True
    else:
        try:
            del request.session['hijack_history']
            del request.session['is_hijacked_user']
        except KeyError:
            pass
    request.session.modified = True
    redirect_to = request.GET.get('next', getattr(
        settings, 'REVERSE_HIJACK_LOGIN_REDIRECT_URL', getattr(
        settings, 'LOGIN_REDIRECT_URL', '/')))
    return HttpResponseRedirect(redirect_to)


def login_user(request, user):
    ''' hijack mechanism '''
    hijack_history = [request.user.pk]
    if request.session.get('hijack_history'):
        hijack_history = request.session['hijack_history'] + hijack_history
    if not request.user.is_superuser:
        if getattr(settings, "ALLOW_STAFF_TO_HIJACKUSER", False):
            # staff allowed, so check if user is staff
            if not user.is_staff:
                raise PermissionDenied
        else:
            # if user is not super user / staff he should be redirected to the admin login
            raise PermissionDenied # pragma: no cover
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    post_superuser_login.send(sender=None, user_id=user.pk)
    request.session['is_hijacked_user'] = True
    request.session['hijack_history'] = hijack_history
    request.session.modified = True
    redirect_to = request.GET.get('next', getattr(
        settings, 'HIJACK_LOGIN_REDIRECT_URL', getattr(
        settings, 'LOGIN_REDIRECT_URL', '/')))
    return HttpResponseRedirect(redirect_to)


@receiver(user_logged_out)
def logout_user(sender, **kwargs):
    ''' wraps logout signal '''
    user = kwargs['user']
    if hasattr(user, 'id'):
        post_superuser_logout.send(sender=None, user_id=user.pk)


"""
@receiver(post_superuser_logout)
def unset_superuser(sender, **kwargs):
    print kwargs['user_id']
    #account = Account.objects.get(user_ptr_id = kwargs['user_id'])
    #account.superuser_login = True

@receiver(post_superuser_login)
def set_superuser(sender, **kwargs):
    print kwargs['user_id']
    #account = Account.objects.get(user_ptr_id = kwargs['user_id'])
    #account.superuser_login = True
"""
