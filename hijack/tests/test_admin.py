from unittest.mock import MagicMock

from django.urls import reverse

from hijack.contrib.admin import HijackUserAdminMixin
from hijack.tests.test_app.models import Post


class TestHijackUserAdminMixin:
    def test_user_admin(self, admin_client):
        url = reverse("admin:test_app_customuser_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200
        assert b"data-hijack-user" in response.content

    def test_related_user(self, admin_client, admin_user):
        url = reverse("admin:test_app_post_changelist")
        Post.objects.create(author=admin_user)
        response = admin_client.get(url)
        assert response.status_code == 200
        assert b"Hijack admin" in response.content

    def test_get_hijack_success_url__obj_absolute_url(self, rf):
        obj = Post()
        obj.get_absolute_url = MagicMock(return_value="/path/to/obj/")
        admin = HijackUserAdminMixin()
        assert admin.get_hijack_success_url(None, obj) == "/path/to/obj/"

    def test_get_hijack_success_url__obj_no_absolute_url(self, rf):
        obj = Post()
        admin = HijackUserAdminMixin()
        assert admin.get_hijack_success_url(None, obj) == "/accounts/profile/"

    def test_get_hijack_success_url__hijack_success_url(self, rf):
        obj = Post()
        obj.get_absolute_url = MagicMock(return_value="/path/to/obj/")
        admin = HijackUserAdminMixin()
        admin.hijack_success_url = "/custom/success/path/"
        assert admin.get_hijack_success_url(None, obj) == "/custom/success/path/"
