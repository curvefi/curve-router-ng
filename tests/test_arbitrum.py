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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

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
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=base_token)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100