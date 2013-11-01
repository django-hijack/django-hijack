from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, get_backends
from django.core.exceptions import PermissionDenied

def login_user(request, user):
    if not request.user.is_superuser:
        raise PermissionDenied
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    return HttpResponseRedirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))
