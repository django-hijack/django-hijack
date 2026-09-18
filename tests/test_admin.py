import logging
from collections import Counter
from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.context import RequestContext
from django.urls import reverse

from hijack.contrib.admin import HijackUserAdminMixin
from hijack.contrib.admin.apps import HijackAdminConfig
from tests.test_app.models import CustomUser, Post


class TestHijackUserAdminMixin:
    def test_user_admin(self, admin_client):
        url = reverse("admin:test_app_customuser_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200
        assert b"data-hijack-user" in response.content

    @pytest.fixture
    def no_user_admin(self):
        custom_user_admin = admin.site._registry.pop(CustomUser)
        yield
        admin.site._registry[CustomUser] = custom_user_admin

    @pytest.fixture
    def custom_hijack_user_admin(self):
        CustomUserAdmin = admin.site._registry.pop(CustomUser)
        HijackAdmin = type(UserAdmin.__name__, (HijackUserAdminMixin, UserAdmin), {})
        HijackAdmin.__module__ = UserAdmin.__module__
        admin.site.register(CustomUser, HijackAdmin)
        yield
        admin.site.unregister(CustomUser)
        admin.site._registry[CustomUser] = CustomUserAdmin

    def test_user_admin__unregistered(self, no_user_admin, admin_client):
        with pytest.warns(UserWarning, match="CustomUser is not registered"):
            HijackAdminConfig.ready(None)

    def test_user_admin__custom_subclass(
        self, custom_hijack_user_admin, admin_client, caplog
    ):
        with caplog.at_level(logging.DEBUG):
            HijackAdminConfig.ready(None)
        assert (
            "UserModelAdmin already is a subclass of HijackUserAdminMixin."
            in caplog.text
        )

    def test_related_user(self, admin_client, admin_user):
        url = reverse("admin:test_app_post_changelist")
        Post.objects.create(author=admin_user)
        response = admin_client.get(url)
        assert response.status_code == 200
        assert b"impersonate admin" in response.content

    def test_get_hijack_button_context(self, rf, admin_user):
        request = rf.get("/")
        request.user = admin_user
        hijack_admin = HijackUserAdminMixin()
        hijack_admin.model = CustomUser

        context = hijack_admin.get_hijack_button_context(request, admin_user)

        assert context["request"] is request
        assert context["another_user"] == admin_user
        assert context["can_hijack"] is True
        assert context["username"] == str(admin_user)
        assert context["is_user_admin"] is True
        assert context["next"] == "/accounts/profile/"
        assert context["hijack_url"] == reverse("hijack:acquire")

    def test_user_admin_does_not_render_hijack_button_with_request_context(
        self, admin_client, monkeypatch
    ):
        for index in range(3):
            CustomUser.objects.create(username=f"user-{index}")

        rendered_templates = []
        original_bind_template = RequestContext.bind_template

        @contextmanager
        def bind_template_spy(context, template):
            origin = getattr(template, "origin", None)
            rendered_templates.append(getattr(origin, "template_name", None) or "")
            with original_bind_template(context, template):
                yield

        monkeypatch.setattr(RequestContext, "bind_template", bind_template_spy)

        url = reverse("admin:test_app_customuser_changelist")
        response = admin_client.get(url)

        assert response.status_code == 200
        counts = Counter(rendered_templates)
        assert counts["hijack/contrib/admin/button.html"] == 0

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
