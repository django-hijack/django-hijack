import contextlib

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from django.dispatch import Signal

hijack_started = Signal()
hijack_ended = Signal()


@contextlib.contextmanager
def no_update_last_login():
    """Disconnect any signals to ``update_last_login`` and reconnect them on exit."""
    kw = {"receiver": update_last_login}
    kw_id = {"receiver": update_last_login, "dispatch_uid": "update_last_login"}

    was_connected = user_logged_in.disconnect(**kw)
    was_connected_id = not was_connected and user_logged_in.disconnect(**kw_id)
    yield
    # Restore signal if needed
    if was_connected:
        user_logged_in.connect(**kw)
    elif was_connected_id:
        user_logged_in.connect(**kw_id)
