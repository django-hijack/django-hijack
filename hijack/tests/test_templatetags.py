from django.urls import reverse

from hijack.templatetags import hijack as templatetags


def test_can_hijack__integration(admin_client):
    response = admin_client.get(reverse("test_app:user-list"))
    assert response.status_code == 200
    assert b'<button type="submit">hijack admin</button>' in response.content


def always_false(**kwargs):
    return False


def always_true(**kwargs):
    return True


def test_can_hijack__import_string(settings):
    settings.HIJACK_PERMISSION_CHECK = (
        f"{always_true.__module__}.{always_true.__qualname__}"
    )
    assert templatetags.can_hijack(None, None)

    settings.HIJACK_PERMISSION_CHECK = (
        f"{always_false.__module__}.{always_false.__qualname__}"
    )
    assert not templatetags.can_hijack(None, None)
