import pytest
from utils import _exchange

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


@pytest.mark.parametrize("coin1", ["usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["usdc", "usdt"])
def test_1_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "usdc": 0,
        "usdt": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7f90122bf0700f9e7e1f688fe926940e8839f353"  # 2pool
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["eth", "wsteth"])
@pytest.mark.parametrize("coin2", ["eth", "wsteth"])
def test_1_stable_wsteth(router, coins, margo, coin1, coin2):
    indexes = {
        "eth": 0,
        "wsteth": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x6eb2dc694eb516b16dc9fbc678c60052bbdd7d80"  # wsteth
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["eurs", "2crv"])
@pytest.mark.parametrize("coin2", ["eurs", "2crv"])
def test_1_crypto(router, coins, margo, coin1, coin2):
    indexes = {
        "eurs": 0,
        "2crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xA827a652Ead76c6B0b3D19dba05452E06e25c27e"  # eursusd
    swap_params = [i, j, 1, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["usdt", "wbtc", "eth", "weth"])
@pytest.mark.parametrize("coin2", ["usdt", "wbtc", "eth", "weth"])
def test_1_tricrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "usdt": 0,
        "wbtc": 1,
        "eth": 2,
        "weth": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x960ea3e3C7FB317332d990873d354E18d7645590"  # tricrypto
    swap_params = [i, j, 1, 3, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["eurs", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["eurs", "usdc", "usdt"])
def test_2_crypto(router, coins, margo, coin1, coin2):
    indexes = {
        "eurs": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xA827a652Ead76c6B0b3D19dba05452E06e25c27e"  # eursusd
    zap = "0x25e2e8d104BC1A70492e2BE32dA7c1f8367F9d2c"
    base_pool = "0x7f90122bf0700f9e7e1f688fe926940e8839f353"  # 2pool
    base_token = "0x7f90122bf0700f9e7e1f688fe926940e8839f353"
    swap_params = [i, j, 2, 2, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=base_token)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


def test_route_2_steps(router, coins, margo):
    coin_names = ["usdc", "usdt", "wbtc"]

    pools = [
        "0x7f90122bf0700f9e7e1f688fe926940e8839f353",  # 2pool
        "0x960ea3e3C7FB317332d990873d354E18d7645590",  # tricrypto
    ]
    swap_params = [[0, 1, 1, 1, 2], [0, 1, 1, 2, 3]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5


def test_route_3_steps(router, coins, margo):
    coin_names = ["usdc", "usdt", "eth", "weth"]

    pools = [
        "0x7f90122bf0700f9e7e1f688fe926940e8839f353",  # 2pool
        "0x960ea3e3C7FB317332d990873d354E18d7645590",  # tricrypto
        coins["weth"].address
    ]
    swap_params = [[0, 1, 1, 1, 2], [0, 2, 1, 2, 3], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5


def test_route_4_steps(router, coins, margo):
    coin_names = ["2crv", "usdc", "usdt", "eth", "weth"]

    pools = [
        "0x7f90122bf0700f9e7e1f688fe926940e8839f353",  # 2pool
        "0x7f90122bf0700f9e7e1f688fe926940e8839f353",  # 2pool
        "0x960ea3e3C7FB317332d990873d354E18d7645590",  # tricrypto
        coins["weth"].address
    ]
    swap_params = [[0, 0, 6, 1, 2], [0, 1, 1, 1, 2], [0, 2, 1, 2, 3], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-4
