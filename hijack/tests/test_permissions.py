import pytest
from django.contrib.auth import get_user_model

from hijack import permissions

superuser = get_user_model()(is_superuser=True)
staff_member = get_user_model()(is_staff=True)
regular_user = get_user_model()()
inactive_user = get_user_model()(is_active=False)


@pytest.mark.parametrize(
    "hijacker, hijacked, has_perm",
    [
        (superuser, None, False),
        (superuser, superuser, True),
        (superuser, staff_member, True),
        (superuser, regular_user, True),
        (superuser, inactive_user, False),
        (staff_member, None, False),
        (staff_member, regular_user, False),
        (staff_member, staff_member, False),
        (staff_member, superuser, False),
        (staff_member, inactive_user, False),
        (regular_user, None, False),
        (regular_user, superuser, False),
        (regular_user, staff_member, False),
        (regular_user, regular_user, False),
        (regular_user, inactive_user, False),
    ],
)
def test_superusers_only(hijacker, hijacked, has_perm):
    assert permissions.superusers_only(hijacker=hijacker, hijacked=hijacked) == has_perm


@pytest.mark.parametrize(
    "hijacker, hijacked, has_perm",
    [
        (superuser, None, False),
        (superuser, superuser, True),
        (superuser, staff_member, True),
        (superuser, regular_user, True),
        (superuser, inactive_user, False),
        (staff_member, None, False),
        (staff_member, regular_user, True),
        (staff_member, staff_member, False),
        (staff_member, superuser, False),
        (staff_member, inactive_user, False),
        (regular_user, None, False),
        (regular_user, superuser, False),
        (regular_user, staff_member, False),
        (regular_user, regular_user, False),
        (regular_user, inactive_user, False),
    ],
)
def test_superusers_and_staff(hijacker, hijacked, has_perm):
    assert (
        permissions.superusers_and_staff(hijacker=hijacker, hijacked=hijacked)
        == has_perm
    )
