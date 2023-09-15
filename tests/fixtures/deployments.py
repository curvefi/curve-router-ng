import pytest
from brownie import ZERO_ADDRESS


INIT_DATA = {
    "ethereum": {
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
        "snx_coins": [
            "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",  # sUSD
            "0xD71eCFF9342A5Ced620049e616c5035F1dB98620",  # sEUR
            "0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb",  # sETH
            "0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6",  # sBTC
        ]
    },
    "optimism": {
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
        "snx_coins": [
            "0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9",  # sUSD
            "0xFBc4198702E81aE77c06D58f81b629BDf36f0a71",  # sEUR
            "0xe405de8f52ba7559f9df3c368500b6e6ae6cee49",  # sETH
            "0x298b9b95708152ff6968aafd889c6586e9169f1d",  # sBTC
        ]
    },
    "xdai": {
        "tricrypto_meta_pools": ["0x5633E00994896D0F472926050eCb32E38bef3e65", ZERO_ADDRESS],  # tricrypto
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    },
    "polygon": {
        "tricrypto_meta_pools": ["0x92215849c439E1f8612b6646060B4E3E5ef822cC", ZERO_ADDRESS],  # atricrypto3
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    },
    "arbitrum": {
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    },
    "avalanche": {
        "tricrypto_meta_pools": ["0xB755B949C126C04e0348DD881a5cF55d424742B2", "0x204f0620e7e7f07b780535711884835977679bba"],  # atricrypto, avaxcrypto
        "stable_calc": "0xCA8d0747B5573D69653C3aC22242e6341C36e4b4",
        "crypto_calc": "0xA72C85C258A81761433B4e8da60505Fe3Dd551CC",
    }
}


@pytest.fixture(scope="module")
def router(Router, RouterOptimism, RouterSidechain, RouterSidechainTricryptoMeta, alice, network, weth):
    stable_calc = INIT_DATA[network]["stable_calc"]
    crypto_calc = INIT_DATA[network]["crypto_calc"]
    if network == "ethereum":
        snx_coins = INIT_DATA[network]["snx_coins"]
        return Router.deploy(weth[network], stable_calc, crypto_calc, snx_coins, {'from': alice})
    if network == "optimism":
        snx_coins = INIT_DATA[network]["snx_coins"]
        return RouterOptimism.deploy(weth[network], stable_calc, crypto_calc, snx_coins, {'from': alice})
    elif "tricrypto_meta_pools" in INIT_DATA[network]:
        tricrypto_meta_pools = INIT_DATA[network]["tricrypto_meta_pools"]
        return RouterSidechainTricryptoMeta.deploy(weth[network], stable_calc, crypto_calc, tricrypto_meta_pools, {'from': alice})
    else:
        return RouterSidechain.deploy(weth[network], stable_calc, crypto_calc, {'from': alice})
