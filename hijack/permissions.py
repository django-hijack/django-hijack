def superusers_only(*, hijacker, hijacked):
    """Superusers may impersonate any other user."""
    if not hijacked:
        return False
    return hijacked.is_active and hijacker.is_superuser


def superusers_and_staff(*, hijacker, hijacked):
    """
    Superusers and staff members may impersonate other users.

    A superuser may impersonate any other user.
    A staff member may impersonate any user, except another staff member or superuser.
    """
    if not hijacked or not hijacked.is_active:
        return False

    if hijacker.is_superuser:
        return True

    return hijacker.is_staff and not (hijacked.is_staff or hijacked.is_superuser)
