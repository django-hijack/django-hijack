def superusers_only(*, hijacker=None, hijacked=None):
    """Superusers may hijack any other user."""
    return hijacker.is_superuser


def superusers_and_staff(*, hijacker=None, hijacked=None):
    """
    Superusers and staff members may hijack other users.

    A superuser may hijack any other user.
    A staff member may hijack any user, except another staff member or superuser.
    """
    if hijacker.is_superuser:
        return True

    return hijacker.is_staff and not (hijacked.is_staff or hijacked.is_superuser)
