from importlib import import_module

import pytest
from django.urls import reverse_lazy


class TestAcquireUserView:
    url = reverse_lazy("hijack:acquire")
    user_detail_url = reverse_lazy("test_app:user-detail")

    def test_acquire(self, admin_client, bob):
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(
            self.url,
            {
                "user_pk": bob.pk,
            },
        )
        assert response.status_code == 302
        assert admin_client.get(self.user_detail_url).content == b'{"username": "bob"}'

    def test_acquire__denied(self, eve_client, bob):
        assert eve_client.get(self.user_detail_url).content == b'{"username": "eve"}'
        response = eve_client.post(
            self.url,
            {
                "user_pk": bob.pk,
            },
        )
        assert response.status_code == 403
        assert eve_client.get(self.user_detail_url).content == b'{"username": "eve"}'

    def test_success_url__default(self, admin_client, bob):
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(
            self.url,
            {
                "user_pk": bob.pk,
            },
        )
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


class TestReleaseUserView:
    url = reverse_lazy("hijack:release")
    user_detail_url = reverse_lazy("test_app:user-detail")

    def test_get__405(self, admin_client):
        assert admin_client.get(self.url).status_code == 405

    def test_post__not_hijacked(self, admin_client):
        assert admin_client.post(self.url).status_code == 404

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
        session["is_hijacked_user"] = True
        session.save()

        response = bob_client.post(self.url)
        assert response.status_code == 302
        assert not bob_client.session.get("hijack_history")
        assert bob_client.get(self.user_detail_url).content == b'{"username": "alice"}'

    def test_success_url__default(self, bob_client, alice):
        session = bob_client.session
        session["hijack_history"] = [str(alice.pk)]
        session["is_hijacked_user"] = True
        session.save()
        assert bob_client.get(self.user_detail_url).content == b'{"username": "bob"}'
        response = bob_client.post(self.url)
        assert response.status_code == 302
        assert response["Location"] == "/hello/bye-bye"

    def test_success_url__next(self, bob_client, alice):
        session = bob_client.session
        session["hijack_history"] = [str(alice.pk)]
        session["is_hijacked_user"] = True
        session.save()
        assert bob_client.get(self.user_detail_url).content == b'{"username": "bob"}'
        response = bob_client.post(self.url, {"next": "/somewhere/else"})
        assert response.status_code == 302
        assert response["Location"] == "/somewhere/else"


class TestIntegration:
    acquire_url = reverse_lazy("hijack:acquire")
    release_url = reverse_lazy("hijack:release")

    user_detail_url = reverse_lazy("test_app:user-detail")

    def test_acquire_release(self, settings, admin_client, bob, alice):
        settings.HIJACK_PERMISSION_CHECK = "hijack.tests.test_app.permissions.allow_all"
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
        response = admin_client.post(
            self.acquire_url,
            {
                "user_pk": bob.pk,
            },
        )
        assert response.status_code == 302
        assert admin_client.get(self.user_detail_url).content == b'{"username": "bob"}'

        response = admin_client.post(
            self.acquire_url,
            {
                "user_pk": alice.pk,
            },
        )
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
        assert response.status_code == 404
        assert (
            admin_client.get(self.user_detail_url).content == b'{"username": "admin"}'
        )
