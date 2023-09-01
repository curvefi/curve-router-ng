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
    second_base_pools = _format_pools([second_base_pool or ZERO_ADDRESS])
    second_base_tokens = _format_pools([second_base_token or ZERO_ADDRESS])
    amount = (amount or 100) * 10**_get_decimals(coin1)
    value = amount if coin1 == ETH_ADDRESS else 0

    initial_balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]
    expected = router.get_dy(route, swap_params, amount, pools)
    required = router.get_dx(route, swap_params, expected, pools, base_pools, base_tokens, second_base_pools, second_base_tokens)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, pools, {"from": margo, "value": value})
    if test_slippage:
        with brownie.reverts("Slippage"):
            router.exchange(route, swap_params, amount, expected * 1001 // 1000, pools, {"from": margo, "value": value})
    balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]

    return amount, expected, required, initial_balances, balances


@pytest.mark.parametrize("coin1", ["amdai", "amusdc", "amusdt"])
@pytest.mark.parametrize("coin2", ["amdai", "amusdc", "amusdt"])
def test_1_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "amdai": 0,
        "amusdc": 1,
        "amusdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-7
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-6


@pytest.mark.parametrize("coin1", ["dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["dai", "usdc", "usdt"])
def test_2_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 2, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-7


@pytest.mark.parametrize("coin1", ["dai", "usdc", "usdt", "wbtc", "weth"])
@pytest.mark.parametrize("coin2", ["dai", "usdc", "usdt", "wbtc", "weth"])
def test_2_tricrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
        "wbtc": 3,
        "weth": 4,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x92215849c439E1f8612b6646060B4E3E5ef822cC"  # atricrypto3
    zap = "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8"
    base_pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 2, 3, 5]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=coins["am3crv"], amount=1)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin1", ["mimatic", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["mimatic", "dai", "usdc", "usdt"])
def test_3_stable_mai(router, coins, margo, coin1, coin2):
    indexes = {
        "mimatic": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x447646e84498552e62ecf097cc305eabfff09308"  # MAI+3pool (factory-v2-107)
    zap = "0x5ab5C56B9db92Ba45a0B46a207286cD83C15C939"
    base_pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 3, 1, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=coins["am3crv"])

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin1", ["usdr", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["usdr", "dai", "usdc", "usdt"])
def test_3_stable_usdr(router, coins, margo, coin1, coin2):
    indexes = {
        "usdr": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xa138341185a9d0429b0021a11fb717b225e13e1f"  # USDR+3pool (factory-v2-339)
    zap = "0x5ab5C56B9db92Ba45a0B46a207286cD83C15C939"
    base_pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 3, 1, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=coins["am3crv"])

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin1", ["crv", "dai", "usdc", "usdt", "wbtc", "weth"])
@pytest.mark.parametrize("coin2", ["crv", "dai", "usdc", "usdt", "wbtc", "weth"])
def test_3_crypto_crv(router, coins, margo, coin1, coin2):
    indexes = {
        "crv": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
        "wbtc": 4,
        "weth": 5,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xc7c939a474cb10eb837894d1ed1a77c61b268fa7"  # crv/tricrypto
    zap = "0x3d8EADb739D1Ef95dd53D718e4810721837c69c1"  # atricrypto3 meta zap
    base_pool = "0x92215849c439E1f8612b6646060B4E3E5ef822cC"  # atricrypto3
    base_pool_zap = "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8"  # atricrypto3 zap
    second_base_pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 3, 2, 6]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=base_pool_zap,
                  second_base_pool=second_base_pool, second_base_token=coins["am3crv"],
                  amount=1, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-2


@pytest.mark.parametrize("coin1", ["matic", "dai", "usdc", "usdt", "wbtc", "weth"])
@pytest.mark.parametrize("coin2", ["matic", "dai", "usdc", "usdt", "wbtc", "weth"])
def test_3_crypto_matic(router, coins, margo, coin1, coin2):
    indexes = {
        "matic": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
        "wbtc": 4,
        "weth": 5,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7bbc0e92505b485aeb3e82e828cb505daf1e50c6"  # wmatic/tricrypto
    zap = "0x3d8EADb739D1Ef95dd53D718e4810721837c69c1"  # atricrypto3 meta zap
    base_pool = "0x92215849c439E1f8612b6646060B4E3E5ef822cC"  # atricrypto3
    base_pool_zap = "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8"  # atricrypto3 zap
    second_base_pool = "0x445FE580eF8d70FF569aB36e80c647af338db351"  # aave
    swap_params = [i, j, 3, 2, 6]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin1, coin2, pool, swap_params,
                  zap=zap, base_pool=base_pool, base_token=base_pool_zap,
                  second_base_pool=second_base_pool, second_base_token=coins["am3crv"],
                  amount=1, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-2
