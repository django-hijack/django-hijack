import datetime
import time
from importlib import import_module
from unittest.mock import MagicMock
from urllib.parse import urlencode, urlunparse

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import connections
from django.shortcuts import resolve_url
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from hijack import views


class TestLockUserTableMixin:
    @pytest.mark.django_db(transaction=True)
    def test_dispatch__custom_manager(self, admin_user, rf):
        class LockedView(views.LockUserTableMixin, View):
            pass

        request = rf.get("/")
        request.user = admin_user
        LockedView().dispatch(request)


class TestSuccessUrlMixin:
    def test_get_success_url__path(self):
        view = views.SuccessUrlMixin()
        get_redirect_url = MagicMock()
        get_redirect_url.return_value = ""
        setattr(view, "get_redirect_url", get_redirect_url)
        assert view.get_success_url() == "/"

    def test_get_success_url__pattern(self):
        view = views.SuccessUrlMixin()
        view.success_url = "bye-bye"
        get_redirect_url = MagicMock()
        get_redirect_url.return_value = ""
        setattr(view, "get_redirect_url", get_redirect_url)
        assert view.get_success_url() == "/bye-bye/"


class TestAcquireUserView:
    url = reverse_lazy("hijack:acquire")
    user_detail_url = reverse_lazy("user-detail")

    def test_acquire(self, admin_client, bob):
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(self.url, {"user_pk": bob.pk})
        assert response.status_code == 302
        assert admin_client.get(self.user_detail_url).content == b'{"username": "bob"}'

    def test_acquire__denied(self, eve_client, bob):
        assert eve_client.get(self.user_detail_url).content == b'{"username": "eve"}'
        response = eve_client.post(self.url, {"user_pk": bob.pk})
        assert response.status_code == 403
        assert eve_client.get(self.user_detail_url).content == b'{"username": "eve"}'

    def test_success_url__default(self, admin_client, bob):
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(self.url, {"user_pk": bob.pk})
        assert response.status_code == 302
        assert response["Location"] == "/accounts/profile/"

    def test_success_url__next(self, admin_client, bob):
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(
            self.url,
            {"user_pk": bob.pk, "next": "/somewhere/over/the/rainbow"},
        )
        assert response.status_code == 302
        assert response["Location"] == "/somewhere/over/the/rainbow"

    def test_dispatch__400(self, admin_client):
        response = admin_client.post(self.url)
        assert response.status_code == 400

    def test_unauthenticated(self, client, bob):
        response = client.post(self.url, {"user_pk": bob.pk})
        assert response.status_code == 302
        assert response["Location"] == urlunparse(
            (
                "",
                "",
                resolve_url(settings.LOGIN_URL),
                "",
                urlencode({"next": self.url}, safe="/"),
                "",
            ),
        )

    @pytest.mark.django_db(databases=["default", "other"])
    def test_locking_secondary_db(self, other_db_router):
        # Users are in the "other" db since we're using the other_db_router fixture.
        james = get_user_model().objects.create(username="james")
        frank = get_user_model().objects.create(
            username="frank", is_staff=True, is_superuser=True
        )
        frank_client = Client()
        frank_client.force_login(frank)
        assert (
            frank_client.get(self.user_detail_url).content == b'{"username": "frank"}'
        )

        with (
            CaptureQueriesContext(connections["default"]) as ctx_default,
            CaptureQueriesContext(connections["other"]) as ctx_other,
        ):
            response = frank_client.post(self.url, {"user_pk": james.pk})

        # Ensure that transaction.atomic was routed to the "other" db.
        assert any("SAVEPOINT" in query["sql"] for query in ctx_other.captured_queries)
        # Ensure no queries were made against the "default" db.
        assert len(ctx_default.captured_queries) == 0
        assert response.status_code == 302
        assert (
            frank_client.get(self.user_detail_url).content == b'{"username": "james"}'
        )


class TestReleaseUserView:
    release_url = reverse_lazy("hijack:release")
    acquire_url = reverse_lazy("hijack:acquire")
    user_detail_url = reverse_lazy("user-detail")

    def test_get__405(self, admin_client, alice):
        admin_client.post(self.acquire_url, {"user_pk": alice.pk})
        assert admin_client.get(self.release_url).status_code == 405

    def test_post__not_hijacked(self, admin_client):
        assert admin_client.post(self.release_url).status_code == 403

    @pytest.fixture
    def hijacked_user(self, client, settings):
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()

        return store

    def test_post__hijacked(self, bob_client, alice):
        assert bob_client.get(self.user_detail_url).content == b'{"username": "bob"}'
        session = bob_client.session
        session["hijack_history"] = [str(alice.pk)]
        session.save()

        response = bob_client.post(self.release_url)
        assert response.status_code == 302
        assert not bob_client.session.get("hijack_history")
        assert bob_client.get(self.user_detail_url).content == b'{"username": "alice"}'

    def test_success_url__default(self, bob_client, alice):
        session = bob_client.session
        session["hijack_history"] = [str(alice.pk)]
        session.save()
        assert bob_client.get(self.user_detail_url).content == b'{"username": "bob"}'
        response = bob_client.post(self.release_url)
        assert response.status_code == 302
        assert response["Location"] == "/bye-bye/"

    def test_success_url__next(self, bob_client, alice):
        session = bob_client.session
        session["hijack_history"] = [str(alice.pk)]
        session.save()
        assert bob_client.get(self.user_detail_url).content == b'{"username": "bob"}'
        response = bob_client.post(self.release_url, {"next": "/somewhere/else"})
        assert response.status_code == 302
        assert response["Location"] == "/somewhere/else"

    def test_unauthenticated(self, client, alice):
        response = client.post(self.release_url, {"user_pk": alice.pk})
        assert response.status_code == 403


class TestIntegration:
    acquire_url = reverse_lazy("hijack:acquire")
    release_url = reverse_lazy("hijack:release")

    user_detail_url = reverse_lazy("user-detail")

    def test_acquire_release(self, settings, admin_client, bob, alice):
        settings.HIJACK_PERMISSION_CHECK = "hijack.tests.test_app.permissions.allow_all"
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(self.acquire_url, {"user_pk": bob.pk})
        assert response.status_code == 302
        assert admin_client.get(self.user_detail_url).content == b'{"username": "bob"}'

        response = admin_client.post(self.acquire_url, {"user_pk": alice.pk})
        assert response.status_code == 302
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "alice"}'
        )

        response = admin_client.post(self.release_url)
        assert response.status_code == 302
        assert admin_client.get(self.user_detail_url).content == b'{"username": "bob"}'

        response = admin_client.post(self.release_url)
        assert response.status_code == 302
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )

        response = admin_client.post(self.release_url)
        assert response.status_code == 403
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )

    def test_keep_session_age(self, admin_client, bob, settings):
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore(
            admin_client.cookies[settings.SESSION_COOKIE_NAME].value
        )
        expire_date = timezone.now() + datetime.timedelta(hours=30)
        session.set_expiry(expire_date)
        session.save()
        time.sleep(0.1)
        admin_client.post(self.acquire_url, {"user_pk": bob.pk})
        assert expire_date == Session.objects.get().expire_date
        time.sleep(0.1)
        admin_client.post(self.release_url)
        assert expire_date == Session.objects.get().expire_date
