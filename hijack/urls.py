from django.contrib.auth import get_user_model
from django.db import models
from django.urls import path, re_path

from hijack import settings as hijack_settings, views


def _get_user_url_pattern(pk=None, pattern=None):
    pk = pk or get_user_model()._meta.pk
    pattern = pattern or hijack_settings.HIJACK_USER_URL_PATTERN

    if pattern:
        return re_path(pattern, views.acquire_user_view, name="acquire")
    elif isinstance(pk, (models.IntegerField, models.AutoField)):
        return path("acquire/<int:pk>/", views.acquire_user_view, name="acquire")
    elif isinstance(pk, models.UUIDField):
        return path("acquire/<uuid:pk>/", views.acquire_user_view, name="acquire")
    elif isinstance(pk, models.SlugField):
        return path("acquire/<slug:pk>/", views.acquire_user_view, name="acquire")
    elif isinstance(pk, models.CharField):
        return path("acquire/<str:pk>/", views.acquire_user_view, name="acquire")
    else:
        raise NotImplementedError(
            f"User model's primary key type {type(pk).__qualname__} is not supported."
            " Please provide your own HIJACK_USER_URL_PATTERN setting."
        )


app_name = "hijack"
urlpatterns = [
    _get_user_url_pattern(),
    path("release/", views.release_user_view, name="release"),
    path("release-hijack/", views.release_hijack, name="release_hijack"),
]

if hijack_settings.HIJACK_DISPLAY_WARNING:
    urlpatterns.append(
        path(
            "disable-hijack-warning/",
            views.disable_hijack_warning,
            name="disable_hijack_warning",
        )
    )

hijacking_user_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES
if "email" in hijacking_user_attributes:
    urlpatterns.append(
        re_path(
            r"^email/(?P<email>[^@\s]+@[^@\s]+\.[^@\s]+)/$",
            views.login_with_email,
            name="login_with_email",
        )
    )
if "username" in hijacking_user_attributes:
    urlpatterns.append(
        re_path(
            r"^username/(?P<username>.*)/$",
            views.login_with_username,
            name="login_with_username",
        )
    )
if "user_id" in hijacking_user_attributes:
    urlpatterns.append(
        re_path(r"^(?P<user_id>[\w-]+)/$", views.login_with_id, name="login_with_id")
    )
