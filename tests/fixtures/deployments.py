import pytest


@pytest.fixture(scope="module")
def router(Router, alice):
    return Router.deploy({'from': alice})
