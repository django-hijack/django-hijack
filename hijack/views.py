import warnings

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from hijack.decorators import hijack_decorator, hijack_require_http_methods
from hijack.helpers import (
    login_user,
    redirect_to_next,
    release_hijack as release_hijack_fx,
)


@hijack_decorator
@hijack_require_http_methods
def acquire_user_view(request, **kwargs):
    user = get_object_or_404(get_user_model(), **kwargs)
    return login_user(request, user)


@login_required
@hijack_require_http_methods
def release_user_view(request):
    return release_hijack_fx(request)


@login_required
@hijack_require_http_methods
def disable_hijack_warning(request):
    request.session["display_hijack_warning"] = False
    return redirect_to_next(request, default_url="/")


def login_with_id(request, user_id):
    warnings.warn(
        '"login_with_id" has been deprecated in favor of "acquire_user_view".',
        DeprecationWarning,
    )
    return acquire_user_view(request, pk=user_id)


def login_with_email(request, email):
    warnings.warn(
        '"login_with_email" has been deprecated in favor of "acquire_user_view".',
        DeprecationWarning,
    )
    return acquire_user_view(request, email=email)


def login_with_username(request, username):
    warnings.warn(
        '"login_with_username" has been deprecated in favor of "acquire_user_view".',
        DeprecationWarning,
    )
    return acquire_user_view(request, username=username)


def release_hijack(request):
    warnings.warn(
        '"release_hijack" has been deprecated in favor of "release_user_view".',
        DeprecationWarning,
    )
    return release_user_view(request)
