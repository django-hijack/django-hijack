from unittest.mock import patch

import pytest
from django.urls import reverse

from hijack.templatetags import hijack as templatetags

from .test_app.permissions import (
    allow_all,
    deny_all,
    require_request_required,
    require_request_optional,
)


def test_can_hijack__integration(admin_client):
    response = admin_client.get(reverse("user-list"))
    assert response.status_code == 200
    assert b'<button type="submit">hijack admin</button>' in response.content


def test_can_hijack_tag__integration(admin_client):
    response = admin_client.get(reverse("user-list-tag"))
    assert response.status_code == 200
    assert b'<button type="submit">hijack admin</button>' in response.content


def test_can_hijack__import_string(settings):
    settings.HIJACK_PERMISSION_CHECK = (
        f"{allow_all.__module__}.{allow_all.__qualname__}"
    )
    assert templatetags.can_hijack(None, None)

    settings.HIJACK_PERMISSION_CHECK = f"{deny_all.__module__}.{deny_all.__qualname__}"
    assert not templatetags.can_hijack(None, None)


def test_can_hijack_tag__no_use_request(settings, rf):
    """
    request is not passed to the permission check function if not a kwarg of it.
    """
    request = rf.get("/")
    settings.HIJACK_PERMISSION_CHECK = (
        f"{allow_all.__module__}.{allow_all.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.allow_all", autospec=True
    ) as allow_all_func:
        templatetags.can_hijack_tag({"request": request}, None, None)
        allow_all_func.assert_called_once_with(hijacker=None, hijacked=None)


def test_can_hijack_tag__use_request(settings, rf):
    """
    request is passed to the permission check function if it's a function kwarg.
    """
    request = rf.get("/")
    settings.HIJACK_PERMISSION_CHECK = (
        f"{require_request_required.__module__}.{require_request_required.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.require_request_required", autospec=True
    ) as require_request_func:
        templatetags.can_hijack_tag({"request": request}, None, None)
        require_request_func.assert_called_once_with(
            hijacker=None, hijacked=None, request=request
        )


def test_can_hijack_tag__use_request_optional(settings, rf):
    """
    request is passed to the permission check function if it's a function kwarg.
    """
    request = rf.get("/")
    settings.HIJACK_PERMISSION_CHECK = (
        f"{require_request_optional.__module__}.{require_request_optional.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.require_request_optional", autospec=True
    ) as require_request_func:
        templatetags.can_hijack_tag({"request": request}, None, None)
        require_request_func.assert_called_once_with(
            hijacker=None, hijacked=None, request=request
        )


def test_can_hijack_filter__no_use_request(settings):
    """
    request is not passed to the permission check function if not a kwarg of it.
    """
    settings.HIJACK_PERMISSION_CHECK = (
        f"{allow_all.__module__}.{allow_all.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.allow_all", autospec=True
    ) as allow_all_func:
        templatetags.can_hijack(None, None)
        allow_all_func.assert_called_once_with(hijacker=None, hijacked=None)


def test_can_hijack_filter__use_request(settings):
    """
    If request argument is required, calling the filter will result in an exception.

    request object is not available in the template filter.
    """
    settings.HIJACK_PERMISSION_CHECK = (
        f"{require_request_required.__module__}.{require_request_required.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.require_request_required", autospec=True
    ) as require_request_func:
        with pytest.raises(TypeError):
            templatetags.can_hijack(None, None)
        require_request_func.assert_not_called()


def test_can_hijack_filter__use_request_optional(settings):
    """
    When using the filter, the request is not passed to the permission check function.

    If request argument is optional, the check is run without the request argument.
    """
    settings.HIJACK_PERMISSION_CHECK = (
        f"{require_request_optional.__module__}.{require_request_optional.__qualname__}"
    )
    with patch(
        "hijack.tests.test_app.permissions.require_request_optional", autospec=True
    ) as require_request_func:
        templatetags.can_hijack(None, None)
        require_request_func.assert_called_once_with(hijacker=None, hijacked=None)
