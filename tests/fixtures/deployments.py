import pytest
from brownie import ZERO_ADDRESS


@pytest.fixture(scope="module")
def router(Router, alice):
    weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    stable_calc = "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4"
    crypto_calc = "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC"
    return Router.deploy(weth, stable_calc, crypto_calc, [ZERO_ADDRESS, ZERO_ADDRESS], {'from': alice})
