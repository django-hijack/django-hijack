import pytest
from django.db import models

from hijack.urls import _get_user_url_pattern


def test__get_user_url_pattern__int_pk_url():
    assert _get_user_url_pattern().pattern.match("acquire/123/")
    assert not _get_user_url_pattern().pattern.match(
        "acquire/f545f538-ece0-4883-93d0-c55a13df60a4/"
    )
    assert not _get_user_url_pattern().pattern.match("acquire/user-slug/")


def test__get_user_url_pattern__uuid_pk_url():
    assert _get_user_url_pattern(pk=models.UUIDField()).pattern.match(
        "acquire/f545f538-ece0-4883-93d0-c55a13df60a4/"
    )
    assert not _get_user_url_pattern(pk=models.UUIDField()).pattern.match(
        "acquire/123/"
    )
    assert not _get_user_url_pattern(pk=models.UUIDField()).pattern.match(
        "acquire/user-slug/"
    )


def test__get_user_url_pattern__slug_pk_url():
    assert _get_user_url_pattern(pk=models.SlugField()).pattern.match(
        "acquire/user-slug/"
    )


def test__get_user_url_pattern__str_pk_url():
    assert _get_user_url_pattern(pk=models.CharField()).pattern.match(
        "acquire/user-slug/"
    )


def test__get_user_url_pattern__custom_pattern():
    assert _get_user_url_pattern(pattern=r"^acquire/(?P<username>\w+)/$").pattern.match(
        "acquire/spiderman/"
    )
    assert not _get_user_url_pattern(
        pattern=r"^acquire/(?P<username>\w+)/$"
    ).pattern.match("acquire/spider-man/")


def test__get_user_url_pattern__raise_not_implemented_error():
    with pytest.raises(NotImplementedError) as e:
        _get_user_url_pattern(pk=models.BooleanField())
    assert (
        "User model's primary key type BooleanField is not supported."
        " Please provide your own HIJACK_USER_URL_PATTERN setting." in str(e)
    )
