from unittest.mock import MagicMock

import pytest
from django.contrib.auth import get_user_model

from hijack import views


def test_login_with_id(rf, db, admin_user, monkeypatch):
    request = rf.post("/")
    request.user = admin_user
    login_user = MagicMock()
    monkeypatch.setattr("hijack.views.login_user", login_user)
    user = get_user_model().objects.create(pk=123)
    with pytest.deprecated_call():
        views.login_with_id(request, 123)
    login_user.assert_called_once_with(request, user)


def test_login_with_email(rf, db, admin_user, monkeypatch):
    request = rf.post("/")
    request.user = admin_user
    login_user = MagicMock()
    monkeypatch.setattr("hijack.views.login_user", login_user)
    user = get_user_model().objects.create(email="spiderman@averngers.com")
    with pytest.deprecated_call():
        views.login_with_email(request, "spiderman@averngers.com")
    login_user.assert_called_once_with(request, user)


def test_login_with_username(rf, db, admin_user, monkeypatch):
    request = rf.post("/")
    request.user = admin_user
    login_user = MagicMock()
    monkeypatch.setattr("hijack.views.login_user", login_user)
    user = get_user_model().objects.create(username="spiderman")
    with pytest.deprecated_call():
        views.login_with_username(request, "spiderman")
    login_user.assert_called_once_with(request, user)


def test_release_hijack(rf, monkeypatch):
    request = rf.get("/")
    release_user_view = MagicMock()
    monkeypatch.setattr("hijack.views.release_user_view", release_user_view)
    with pytest.deprecated_call():
        views.release_hijack(request)
    release_user_view.assert_called_once_with(request)
