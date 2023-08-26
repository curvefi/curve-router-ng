import pytest
from brownie import ZERO_ADDRESS, ETH_ADDRESS

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")

MAX_STEPS = 4
ROUTE_LENGTH = MAX_STEPS * 2 + 1


def _format_route(route: list[str]) -> list[str]:
    return route + [ZERO_ADDRESS] * (ROUTE_LENGTH - len(route))


def _format_swap_params(swap_params: list[list[int]]) -> list[list[int]]:
    return swap_params + [[0, 0, 0]] * (MAX_STEPS - len(swap_params))


def _format_pools(pools: list[str]) -> list[str]:
    return pools + [ZERO_ADDRESS] * (MAX_STEPS - len(pools))


def _get_balance(coin, account) -> int:
    return account.balance() if coin == ETH_ADDRESS else coin.balanceOf(account)


def _get_decimals(coin) -> int:
    return 18 if coin == ETH_ADDRESS else coin.decimals()


def _exchange(router, coins, margo, coin1_name, coin2_name, pool, _swap_params, zap=None):
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    if zap is not None:
        route = _format_route([coin1, zap, coin2])
        pools = _format_pools([pool])
    else:
        route = _format_route([coin1, pool, coin2])
        pools = _format_pools([])
    swap_params = _format_swap_params([_swap_params])
    amount = 100 * 10**_get_decimals(coin1)
    value = amount if coin1 == ETH_ADDRESS else 0

    initial_balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]
    expected = router.get_dy(route, swap_params, amount, pools)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, pools, {"from": margo, "value": value})
    balances = [_get_balance(coin1, margo), _get_balance(coin2, margo)]

    return amount, expected, initial_balances, balances


def test_1(router, coins, margo):
    coin1 = "dai"
    coin2 = "usdc"
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [0, 1, 1]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1


def test_1_meta(router, coins, margo):
    coin1 = "usdd"
    coin2 = "3crv"
    pool = "0xe6b5cc1b4b47305c58392ce3d359b10282fc36ea"  # USDD/3crv (factory-v2-116)
    swap_params = [0, 1, 1]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1


def test_1_lending(router, coins, margo):
    coin1 = "cdai"
    coin2 = "usdt"
    pool = "0x52ea46506b9cc5ef470c5bf89f17dc28bb35d85c"  # usdt
    swap_params = [0, 2, 1]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2


def test_2_meta(router, coins, margo):
    coin1 = "usdd"
    coin2 = "usdc"
    pool = "0xe6b5cc1b4b47305c58392ce3d359b10282fc36ea"  # USDD/3crv (factory-v2-116)
    swap_params = [0, 2, 2]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_2_lending(router, coins, margo):
    coin1 = "dai"
    coin2 = "usdt"
    pool = "0x52ea46506b9cc5ef470c5bf89f17dc28bb35d85c"  # usdt
    swap_params = [0, 2, 2]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3(router, coins, margo):
    coin1 = "usdt"
    coin2 = "wbtc"
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [0, 1, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_eth(router, coins, margo):
    coin1 = "eth"
    coin2 = "wbtc"
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [2, 1, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_weth(router, coins, margo):
    coin1 = "weth"
    coin2 = "usdt"
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [2, 0, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_eth_cvxeth(router, coins, margo):
    coin1 = "cvx"
    coin2 = "eth"
    pool = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4"  # cvxeth
    swap_params = [1, 0, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_weth_cvxeth(router, coins, margo):
    coin1 = "cvx"
    coin2 = "weth"
    pool = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4"  # cvxeth
    swap_params = [1, 0, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_meta(router, coins, margo):
    coin1 = "eurt"
    coin2 = "3crv"
    pool = "0x9838eccc42659fa8aa7daf2ad134b53984c9427b"  # eurtusd
    swap_params = [0, 1, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_3_meta_factory(router, coins, margo):
    coin1 = "3crv"
    coin2 = "dchf"
    pool = "0xdcb11e81c8b8a1e06bf4b50d4f6f3bb31f7478c3"  # DCHF/3CRV (factory-crypto-116)
    swap_params = [1, 0, 3]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_4(router, coins, margo):
    coin1 = "eurt"
    coin2 = "usdt"
    pool = "0x5D0F47B32fDd343BfA74cE221808e2abE4A53827"  # eurtusd zap
    swap_params = [0, 3, 4]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_6(router, coins, margo):
    coin1 = "usdt"
    coin2 = "dchf"
    zap = "0x97aDC08FA1D849D2C48C5dcC1DaB568B169b0267"
    pool = "0xdcb11e81c8b8a1e06bf4b50d4f6f3bb31f7478c3"  # DCHF/3CRV (factory-crypto-116)
    swap_params = [3, 0, 6]
    zap_balance = coins[coin2].balanceOf(zap)
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params, zap)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1] - zap_balance) - expected) / expected < 1e-4


def test_7_fraxusdc(router, coins, margo):
    coin1 = "frax"
    coin2 = "fraxbp"
    pool = "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2"  # fraxusdc
    swap_params = [0, 0, 7]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


def test_7_fraxusdp(router, coins, margo):
    coin1 = "usdp"
    coin2 = "fraxusdplp"
    pool = "0xaE34574AC03A15cd58A92DC79De7B1A0800F1CE3"  # fraxusdp
    swap_params = [1, 0, 7]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


def test_7_sbtc2(router, coins, margo):
    coin1 = "wbtc"
    coin2 = "sbtc2lp"
    pool = "0xf253f83AcA21aAbD2A20553AE0BF7F65C755A07F"  # sbtc2
    swap_params = [0, 0, 7]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3


def test_8(router, coins, margo):
    coin1 = "usdc"
    coin2 = "3crv"
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [1, 0, 8]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


def test_12_fraxusdc(router, coins, margo):
    coin1 = "fraxbp"
    coin2 = "frax"
    pool = "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2"  # fraxusdc
    swap_params = [0, 0, 12]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


def test_12_fraxusdp(router, coins, margo):
    coin1 = "fraxusdplp"
    coin2 = "usdp"
    pool = "0xaE34574AC03A15cd58A92DC79De7B1A0800F1CE3"  # fraxusdp
    swap_params = [0, 1, 12]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


def test_12_sbtc2(router, coins, margo):
    coin1 = "sbtc2lp"
    coin2 = "wbtc"
    pool = "0xf253f83AcA21aAbD2A20553AE0BF7F65C755A07F"  # sbtc2
    swap_params = [0, 0, 12]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3


def test_12_3pool(router, coins, margo):
    coin1 = "3crv"
    coin2 = "usdc"
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [0, 1, 12]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4


@pytest.mark.parametrize("coin1", ["eth", "weth"])
@pytest.mark.parametrize("coin2", ["eth", "weth"])
def test_15(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["weth"]
    swap_params = [0, 0, 15]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


def test_16_steth(router, coins, margo):
    coin1 = "eth"
    coin2 = "steth"
    pool = coins[coin2].address
    swap_params = [0, 0, 16]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2


def test_16_frxeth(router, coins, margo):
    coin1 = "eth"
    coin2 = "frxeth"
    pool = "0xbAFA44EFE7901E04E39Dad13167D089C559c1138"  # frxeth minter
    swap_params = [0, 0, 16]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


@pytest.mark.parametrize("coin1", ["steth", "wsteth"])
@pytest.mark.parametrize("coin2", ["steth", "wsteth"])
def test_17_wsteth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["wsteth"].address
    swap_params = [0, 0, 17]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) <= 1
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2


@pytest.mark.parametrize("coin1", ["frxeth", "sfrxeth"])
@pytest.mark.parametrize("coin2", ["frxeth", "sfrxeth"])
def test_17_sfrxeth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["sfrxeth"].address
    swap_params = [0, 0, 17]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6


@pytest.mark.parametrize("coin1", ["susd", "seur", "seth", "sbtc"])
@pytest.mark.parametrize("coin2", ["susd", "seur", "seth", "sbtc"])
def test_18(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"  # SNX
    swap_params = [0, 0, 18]
    amount, expected, initial_balances, balances = _exchange(router, coins, margo, coin1, coin2, pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
