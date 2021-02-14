from django.urls import reverse

from hijack.templatetags import hijack as templatetags

from .test_app.permissions import allow_all, deny_all


def test_can_hijack__integration(admin_client):
    response = admin_client.get(reverse("user-list"))
    assert response.status_code == 200
    assert b'<button type="submit">hijack admin</button>' in response.content


def test_can_hijack__import_string(settings):
    settings.HIJACK_PERMISSION_CHECK = (
        f"{allow_all.__module__}.{allow_all.__qualname__}"
    )
    assert templatetags.can_hijack(None, None)

    settings.HIJACK_PERMISSION_CHECK = f"{deny_all.__module__}.{deny_all.__qualname__}"
    assert not templatetags.can_hijack(None, None)
