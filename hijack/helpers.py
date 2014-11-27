from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import login, get_backends
from django.dispatch import receiver

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from hijack.signals import post_superuser_login
from hijack.signals import post_superuser_logout


def reverseHijack(request):
    if not request.session.get('hijack_dict'):
        raise Http404

    hijack_dict = request.session['hijack_dict']
    user = get_object_or_404(User, pk=hijack_dict.pop())
    #request.user = user

    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    post_superuser_login.send(sender=None, user_id=user.id)
    if hijack_dict:
        request.session['hijack_dict'] = hijack_dict
        request.session['hijackedBySuperuser'] = True
        request.session.modified = True
    return HttpResponseRedirect(getattr(
        settings, 'REVERSE_HIJACK_LOGIN_REDIRECT_URL', getattr(settings, 'LOGIN_REDIRECT_URL', '/')))


def login_user(request, user):
    ''' hijack mechanism '''
    hijack_dict = [request.user.pk]
    if request.session.get('hijack_dict'):
        hijack_dict = request.session['hijack_dict'] + hijack_dict

    if not request.user.is_superuser:
        if getattr(settings, "ALLOW_STAFF_TO_HIJACKUSER", False):
            # staff allowed, so check if user is staff
            if not user.is_staff:
                raise PermissionDenied
        else:
            raise PermissionDenied

    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    post_superuser_login.send(sender=None, user_id=user.id)
    request.session['hijackedBySuperuser'] = True
    request.session['hijack_dict'] = hijack_dict
    request.session.modified = True
    return HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))


@receiver(user_logged_out)
def logout_user(sender, **kwargs):
    ''' wraps logout signal '''
    user = kwargs['user']
    if hasattr(user, 'id'):
        post_superuser_logout.send(sender=None, user_id=user.id)


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
