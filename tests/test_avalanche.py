import pytest
import brownie
from brownie import ZERO_ADDRESS, ETH_ADDRESS

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")

MAX_STEPS = 4
ROUTE_LENGTH = MAX_STEPS * 2 + 1


def _format_route(route: list[str]) -> list[str]:
    return route + [ZERO_ADDRESS] * (ROUTE_LENGTH - len(route))


def _format_swap_params(swap_params: list[list[int]]) -> list[list[int]]:
    return swap_params + [[0, 0, 0, 0, 0]] * (MAX_STEPS - len(swap_params))


def _format_pools(pools: list[str]) -> list[str]:
    return pools + [ZERO_ADDRESS] * (MAX_STEPS - len(pools))


def _get_balance(coin, account) -> int:
    return account.balance() if coin == ETH_ADDRESS else coin.balanceOf(account)


def _get_decimals(coin) -> int:
    return 18 if coin == ETH_ADDRESS else coin.decimals()


def _exchange(router, coins, margo, coin1_name, coin2_name, pool, _swap_params,
              amount=None, zap=None, base_pool=None, base_token=None, second_base_pool=None,
              second_base_token=None, test_slippage=True):
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = _format_route([coin1, zap, coin2]) if zap is not None else _format_route([coin1, pool, coin2])
    swap_params = _format_swap_params([_swap_params])
    pools = _format_pools([pool])
    base_pools = _format_pools([base_pool or ZERO_ADDRESS])
    base_tokens = _format_pools([base_token or ZERO_ADDRESS])
    amount = (amount or 100) * 10**_get_decimals(coin1)
    value = amount if coin1 == ETH_ADDRESS else 0

    initial_balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]
    expected = router.get_dy(route, swap_params, amount, pools)
    required = router.get_dx(route, swap_params, expected, pools, base_pools, base_tokens)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, pools, {"from": margo, "value": value})
    if test_slippage:
        with brownie.reverts("Slippage"):
            router.exchange(route, swap_params, amount, expected * 1001 // 1000, pools, {"from": margo, "value": value})
    balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]

    return amount, expected, required, initial_balances, balances


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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-6

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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  base_pool=base_pool, base_token=coins["av3crv"])

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-6


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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  base_pool=coins["2crv"].address, base_token=coins["2crv"].address, amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-9 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100


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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=coins["av3crv"])

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-3


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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=coins["av3crv"], amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin1", ["usdc", "usdt", "btc.b"])
@pytest.mark.parametrize("coin2", ["usdc", "usdt", "btc.b"])
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
    if i == 3:  # TODO deploy new zap for this pool with use_eth=True by default
        return
    pool = "0x204f0620e7e7f07b780535711884835977679bba"  # avaxcrypto
    zap = "0x25b3D0eeBcd85Ea5A970981c5E2A342f4e1064e8"
    swap_params = [i, j, 2, 3, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=coins["2crv"].address, base_token=coins["2crv"].address, amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


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
        _exchange(router, coins, margo, coin, lp, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


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
        _exchange(router, coins, margo, coin, lp, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


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
        _exchange(router, coins, margo, lp, coin, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


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
        _exchange(router, coins, margo, lp, coin, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3
