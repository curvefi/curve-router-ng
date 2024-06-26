import pytest
from utils import _exchange, ZERO_ADDRESS, _get_balance

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


@pytest.mark.parametrize("coin1", ["avdai", "avusdc", "avusdt"])
@pytest.mark.parametrize("coin2", ["avdai", "avusdc", "avusdt"])
def test_1_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "avdai": 0,
        "avusdc": 1,
        "avusdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-6
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-5 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-5


@pytest.mark.parametrize("coin1", ["nxusd", "av3crv"])
@pytest.mark.parametrize("coin2", ["nxusd", "av3crv"])
def test_1_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "nxusd": 0,
        "av3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x6bf6fc7eaf84174bb7e1610efd865f0ebd2aa96d"  # NXUSD+av3CRV (factory-v2-66)
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["av3crv"])

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-6
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["2crv", "btc.b", "wavax"])
@pytest.mark.parametrize("coin2", ["2crv", "btc.b", "wavax"])
def test_1_tricrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "2crv": 0,
        "btc.b": 1,
        "wavax": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x204f0620e7e7f07b780535711884835977679bba"  # avaxcrypto
    swap_params = [i, j, 1, 3, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=coins["2crv"].address, base_tokens=coins["2crv"].address, amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["dai.e", "usdc.e", "usdt.e"])
@pytest.mark.parametrize("coin2", ["dai.e", "usdc.e", "usdt.e"])
def test_2_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "dai.e": 0,
        "usdc.e": 1,
        "usdt.e": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [i, j, 2, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-9 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["nxusd", "dai.e", "usdc.e", "usdt.e"])
@pytest.mark.parametrize("coin2", ["nxusd", "dai.e", "usdc.e", "usdt.e"])
def test_3_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "nxusd": 0,
        "dai.e": 1,
        "usdc.e": 2,
        "usdt.e": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x6bf6fc7eaf84174bb7e1610efd865f0ebd2aa96d"  # NXUSD+av3CRV (factory-v2-66)
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    zap = "0x001E3BA199B4FF4B5B6e97aCD96daFC0E2e4156e"
    swap_params = [i, j, 3, 1, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["av3crv"])

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["dai.e", "usdc.e", "usdt.e", "wbtc.e", "weth.e"])
@pytest.mark.parametrize("coin2", ["dai.e", "usdc.e", "usdt.e", "wbtc.e", "weth.e"])
def test_2_tricrypto_atricrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "dai.e": 0,
        "usdc.e": 1,
        "usdt.e": 2,
        "wbtc.e": 3,
        "weth.e": 4,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xB755B949C126C04e0348DD881a5cF55d424742B2"  # atricrypto
    zap = "0x58e57cA18B7A47112b877E31929798Cd3D703b0f"
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [i, j, 2, 3, 5]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["av3crv"], amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdc", "usdt", "btc.b", "avax"])
@pytest.mark.parametrize("coin2", ["usdc", "usdt", "btc.b", "avax"])
def test_2_tricrypto_avaxcrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "usdc": 0,
        "usdt": 1,
        "btc.b": 2,
        "avax": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x204f0620e7e7f07b780535711884835977679bba"  # avaxcrypto
    zap = "0x9f2Fa7709B30c75047980a0d70A106728f0Ef2db"
    swap_params = [i, j, 2, 3, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=coins["2crv"].address, base_tokens=coins["2crv"].address, amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin", ["usdc", "usdt"])
def test_4_stable(router, coins, margo, coin):
    indexes = {
        "usdc": 0,
        "usdt": 1,
    }
    i = indexes[coin]
    lp = "2crv"
    pool = coins[lp]  # 2pool
    swap_params = [i, 0, 4, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-15
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["dai.e", "usdc.e", "usdt.e"])
def test_5_stable(router, coins, margo, coin):
    indexes = {
        "dai.e": 0,
        "usdc.e": 1,
        "usdt.e": 2,
    }
    i = indexes[coin]
    lp = "av3crv"
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [i, 0, 5, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["usdc", "usdt"])
def test_6_stable(router, coins, margo, coin):
    indexes = {
        "usdc": 0,
        "usdt": 1,
    }
    j = indexes[coin]
    lp = "2crv"
    pool = coins[lp]  # 2pool
    swap_params = [0, j, 6, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-15
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["dai.e", "usdc.e", "usdt.e"])
def test_7_stable(router, coins, margo, coin):
    indexes = {
        "dai.e": 0,
        "usdc.e": 1,
        "usdt.e": 2,
    }
    j = indexes[coin]
    lp = "av3crv"
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # aave
    swap_params = [0, j, 7, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin1", ["avax", "wavax"])
@pytest.mark.parametrize("coin2", ["avax", "wavax"])
def test_route_8(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["wavax"].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


def test_route_2_steps(router, coins, margo):
    coin_names = ["nxusd", "dai.e", "weth.e"]

    pools = [
        "0x6bf6fc7eaf84174bb7e1610efd865f0ebd2aa96d",  # NXUSD+av3CRV (factory-v2-66)
        "0xB755B949C126C04e0348DD881a5cF55d424742B2",  # atricrypto
    ]
    zaps = [
        "0x001E3BA199B4FF4B5B6e97aCD96daFC0E2e4156e",
        "0x58e57cA18B7A47112b877E31929798Cd3D703b0f",
    ]
    base_pools = [
        "0x7f90122BF0700F9E7e1F688fe926940E8839F353",  # aave
        "0x7f90122BF0700F9E7e1F688fe926940E8839F353",  # aave
    ]
    base_tokens = [
        coins["av3crv"].address,
        coins["av3crv"].address,
    ]
    swap_params = [[0, 1, 3, 1, 4], [0, 4, 2, 3, 5]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  zaps=zaps, base_pools=base_pools, base_tokens=base_tokens)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin_names[-1]], router) == 1


def test_route_3_steps(router, coins, margo):
    coin_names = ["usdt", "usdc", "2crv", "wavax"]

    pools = [
        coins["2crv"],  # 2pool
        coins["2crv"],  # 2pool
        "0x204f0620e7e7f07b780535711884835977679bba",  # avaxcrypto
    ]
    base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        coins["2crv"].address,  # 2pool
    ]
    base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        coins["2crv"].address,
    ]
    swap_params = [[1, 0, 1, 1, 2], [0, 0, 4, 1, 2], [0, 2, 1, 3, 3]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  base_pools=base_pools, base_tokens=base_tokens)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin_names[-1]], router) == 1
