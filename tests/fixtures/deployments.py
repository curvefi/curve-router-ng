import pytest
from brownie import ZERO_ADDRESS

INIT_DATA = {
    "ethereum": {
        "tricrypto_meta_pools": [ZERO_ADDRESS, ZERO_ADDRESS],
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    },
    "polygon": {
        "tricrypto_meta_pools": ["0x92215849c439E1f8612b6646060B4E3E5ef822cC", ZERO_ADDRESS],
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    },
    "arbitrum": {
        "tricrypto_meta_pools": [ZERO_ADDRESS, ZERO_ADDRESS],
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    }
}


@pytest.fixture(scope="module")
def router(Router, alice, network, weth):
    stable_calc = INIT_DATA[network]["stable_calc"]
    crypto_calc = INIT_DATA[network]["crypto_calc"]
    tricrypto_meta_pools = INIT_DATA[network]["tricrypto_meta_pools"]
    return Router.deploy(weth[network], stable_calc, crypto_calc, tricrypto_meta_pools, {'from': alice})
