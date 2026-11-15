import pytest
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login

from hijack.signals import no_update_last_login


def test_no_update_last_login(bob, client):
    assert bob.last_login is None
    with no_update_last_login():
        client.force_login(bob)
    assert bob.last_login is None


def test_no_update_last_login__no_dispatch_uid(bob, client):
    assert bob.last_login is None
    with no_update_last_login():
        user_logged_in.connect(update_last_login)
        with no_update_last_login():
            client.force_login(bob)
    assert bob.last_login is None


@pytest.mark.parametrize("dispatch_uid", ["update_last_login", None])
def test_no_update_last_login__restores_on_exception(bob, client, dispatch_uid):
    user_logged_in.disconnect(update_last_login)
    user_logged_in.disconnect(update_last_login, dispatch_uid="update_last_login")
    user_logged_in.connect(update_last_login, dispatch_uid=dispatch_uid)
    try:
        with pytest.raises(RuntimeError), no_update_last_login():
            raise RuntimeError

        client.force_login(bob)
        bob.refresh_from_db()
        assert bob.last_login is not None
    finally:
        user_logged_in.disconnect(update_last_login, dispatch_uid=dispatch_uid)
        user_logged_in.connect(update_last_login, dispatch_uid="update_last_login")
