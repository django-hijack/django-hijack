from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import login, get_backends
from django.core.exceptions import PermissionDenied


@staff_member_required
def login_as(request, userID):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_object_or_404(User, pk=userID)
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    return HttpResponseRedirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))
