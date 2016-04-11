# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from hijack.decorators import hijack_require_http_methods, hijack_decorator
from hijack.helpers import login_user, redirect_to_next
from hijack.helpers import release_hijack as release_hijack_fx

from compat import get_user_model


@hijack_decorator
@hijack_require_http_methods
def login_with_id(request, user_id):
    # input(user_id) is unicode
    try:
        user_id = int(user_id)
    except ValueError:
        return HttpResponseBadRequest('user_id must be an integer value.')
    user = get_object_or_404(get_user_model(), pk=user_id)
    return login_user(request, user)


@hijack_decorator
@hijack_require_http_methods
def login_with_email(request, email):
    user = get_object_or_404(get_user_model(), email=email)
    return login_user(request, user)


@hijack_decorator
@hijack_require_http_methods
def login_with_username(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return login_user(request, user)


@login_required
@hijack_require_http_methods
def release_hijack(request):
    return release_hijack_fx(request)


@login_required
@hijack_require_http_methods
def disable_hijack_warning(request):
    request.session['display_hijack_warning'] = False
    return redirect_to_next(request, default_url='/')
