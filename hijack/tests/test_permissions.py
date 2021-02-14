import pytest
from django.contrib.auth import get_user_model

from hijack import permissions

superuser = get_user_model()(is_superuser=True)
staff_member = get_user_model()(is_staff=True)
regular_user = get_user_model()()


@pytest.mark.parametrize(
    "hijacker, hijacked, has_perm",
    [
        (superuser, superuser, True),
        (superuser, staff_member, True),
        (superuser, regular_user, True),
        (staff_member, regular_user, False),
        (staff_member, staff_member, False),
        (staff_member, superuser, False),
        (regular_user, superuser, False),
        (regular_user, staff_member, False),
        (regular_user, regular_user, False),
    ],
)
def test_superusers_only(hijacker, hijacked, has_perm):
    assert permissions.superusers_only(hijacker=hijacker, hijacked=hijacked) == has_perm


@pytest.mark.parametrize(
    "hijacker, hijacked, has_perm",
    [
        (superuser, superuser, True),
        (superuser, staff_member, True),
        (superuser, regular_user, True),
        (staff_member, regular_user, True),
        (staff_member, staff_member, False),
        (staff_member, superuser, False),
        (regular_user, superuser, False),
        (regular_user, staff_member, False),
        (regular_user, regular_user, False),
    ],
)
def test_superusers_and_staff(hijacker, hijacked, has_perm):
    assert (
        permissions.superusers_and_staff(hijacker=hijacker, hijacked=hijacked)
        == has_perm
    )
