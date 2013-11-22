from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.contrib.auth import login, get_backends
from django.dispatch import receiver

from signals import post_superuser_login
from signals import post_superuser_logout



def login_user(request, user):
    ''' hijack mechanism '''
    if not request.user.is_superuser:
        raise PermissionDenied
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    post_superuser_login.send(sender=None, user_id = user.id)
    request.session['hijackedBySuperuser'] = True
    request.session.modified = True
    return HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))


@receiver(user_logged_out)
def logout_user(sender, **kwargs):
    ''' wraps logout signal '''
    user = kwargs['user'] 
    post_superuser_logout.send(sender=None, user_id = user.id)
    print 'Successful Logout', user  


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
