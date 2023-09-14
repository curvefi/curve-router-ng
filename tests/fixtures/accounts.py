import pytest


@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def margo(accounts):
    yield accounts[0]
