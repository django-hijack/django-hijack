import pytest
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.fixture()
def alice(db):
    return get_user_model().objects.create(username="alice", is_staff=True)


@pytest.fixture()
def alice_client(alice):
    client = Client()
    client.force_login(alice)
    return client


@pytest.fixture()
def bob(db):
    return get_user_model().objects.create(username="bob", is_staff=False)


@pytest.fixture()
def bob_client(bob):
    client = Client()
    client.force_login(bob)
    return client


@pytest.fixture()
def eve(db):
    return get_user_model().objects.create(username="eve", is_staff=False)


@pytest.fixture()
def eve_client(eve):
    client = Client()
    client.force_login(eve)
    return client
