import pytest
from utils import _exchange, _get_balance

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


@pytest.mark.parametrize("coin1", ["dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["dai", "usdc", "usdt"])
def test_1_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdd", "3crv"])
@pytest.mark.parametrize("coin2", ["usdd", "3crv"])
def test_1_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "usdd": 0,
        "3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xe6b5cc1b4b47305c58392ce3d359b10282fc36ea"  # USDD/3crv (factory-v2-116)
    base_pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, base_pools=base_pool)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["cdai", "cusdc", "usdt"])
@pytest.mark.parametrize("coin2", ["cdai", "cusdc", "usdt"])
def test_1_stable_lending(router, coins, margo, coin1, coin2):
    indexes = {
        "cdai": 0,
        "cusdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x52ea46506b9cc5ef470c5bf89f17dc28bb35d85c"  # usdt
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected <= 1e-6
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["eth", "weth", "cvx"])
@pytest.mark.parametrize("coin2", ["eth", "weth", "cvx"])
def test_1_crypto(router, coins, margo, coin1, coin2):
    if coin1 == coin2 or (coin1 != "cvx" and coin2 != "cvx"):
        return
    i, j = 0, 1
    if coin1 == "cvx":
        i, j = 1, 0
    pool = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4"  # cvxeth
    swap_params = [i, j, 1, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["eurt", "3crv"])
@pytest.mark.parametrize("coin2", ["eurt", "3crv"])
def test_1_crypto_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "eurt": 0,
        "3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x9838eccc42659fa8aa7daf2ad134b53984c9427b"  # eurtusd
    swap_params = [i, j, 1, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["dchf", "3crv"])
@pytest.mark.parametrize("coin2", ["dchf", "3crv"])
def test_1_crypto_meta_factory(router, coins, margo, coin1, coin2):
    indexes = {
        "dchf": 0,
        "3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xdcb11e81c8b8a1e06bf4b50d4f6f3bb31f7478c3"  # DCHF/3CRV (factory-crypto-116)
    swap_params = [i, j, 1, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdt", "wbtc", "eth", "weth"])
@pytest.mark.parametrize("coin2", ["usdt", "wbtc", "eth", "weth"])
def test_1_tricrypto(router, coins, margo, coin1, coin2):
    indexes = {
        "usdt": 0,
        "wbtc": 1,
        "eth": 2,
        "weth": 2
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [i, j, 1, 3, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 2e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["wbtc", "crvusd"])
@pytest.mark.parametrize("coin2", ["wbtc", "crvusd"])
def test_1_llamma_wbtc(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    i, j = 0, 1
    if coin2 == "crvusd":
        i, j = 1, 0
    pool = "0xe0438eb3703bf871e31ce639bd351109c88666ea"  # wbtc llamma
    swap_params = [i, j, 1, 4, 2]
    amount = 1000 if coin1 == "crvusd" else 0.1
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected <= 5e-4
    assert abs(amount - required) / amount < 1e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["weth", "crvusd"])
@pytest.mark.parametrize("coin2", ["weth", "crvusd"])
def test_1_llamma_weth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    i, j = 0, 1
    if coin2 == "crvusd":
        i, j = 1, 0
    pool = "0x1681195c176239ac5e72d9aebacf5b2492e0c4ee"  # weth llamma
    swap_params = [i, j, 1, 4, 2]
    amount = 300 if coin1 == "crvusd" else 0.1
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected <= 5e-4
    assert abs(amount - required) / amount < 1e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdd", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["usdd", "dai", "usdc", "usdt"])
def test_2_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "usdd": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xe6b5cc1b4b47305c58392ce3d359b10282fc36ea"  # USDD/3crv (factory-v2-116)
    base_pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 2, 1, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["3crv"].address)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 2e-5
    assert abs(amount - required) / amount < 2e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["dai", "usdc", "usdt"])
def test_2_stable_lending(router, coins, margo, coin1, coin2):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x52ea46506b9cc5ef470c5bf89f17dc28bb35d85c"  # usdt
    swap_params = [i, j, 2, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected <= 1e-7
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["eurt", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["eurt", "dai", "usdc", "usdt"])
def test_2_crypto(router, coins, margo, coin1, coin2):
    indexes = {
        "eurt": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x9838eCcC42659FA8AA7daF2aD134b53984c9427b"  # eurtusd
    zap = "0x5D0F47B32fDd343BfA74cE221808e2abE4A53827"
    base_pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 2, 2, 4]
    zap_balance = coins[coin2].balanceOf(zap)
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["3crv"].address, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1] - zap_balance) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 1e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["dchf", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["dchf", "dai", "usdc", "usdt"])
def test_3_crypto(router, coins, margo, coin1, coin2):
    indexes = {
        "dchf": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xdcb11e81c8b8a1e06bf4b50d4f6f3bb31f7478c3"  # DCHF/3CRV (factory-crypto-116)
    zap = "0x97aDC08FA1D849D2C48C5dcC1DaB568B169b0267"
    base_pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 3, 2, 4]
    zap_balance = coins[coin2].balanceOf(zap)
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["3crv"].address, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1] - zap_balance) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 1e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin", ["frax", "usdc"])
def test_4_stable_2coins_fraxusdc(router, coins, margo, coin):
    i = 0 if coin == "frax" else 1
    lp = "fraxbp"
    pool = "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2"  # fraxusdc
    swap_params = [i, 0, 4, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 2e-4
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["frax", "usdp"])
def test_4_stable_2coins_fraxusdp(router, coins, margo, coin):
    i = 0 if coin == "frax" else 1
    lp = "fraxusdp_lp"
    pool = "0xaE34574AC03A15cd58A92DC79De7B1A0800F1CE3"  # fraxusdp
    swap_params = [i, 0, 4, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["dai", "usdc", "usdt"])
def test_4_stable_3coins(router, coins, margo, coin):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin]
    lp = "3crv"
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, 0, 4, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["weth", "cvx"])
def test_4_crypto(router, coins, margo, coin):
    indexes = {
        "weth": 0,
        "cvx": 1,
    }
    i = indexes[coin]
    lp = "cvxeth_lp"
    pool = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4"  # cvxeth
    swap_params = [i, 0, 4, 2, 2]
    amount = None if coin == "cvx" else 0.1
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["usdt", "wbtc", "weth"])
def test_4_tricrypto(router, coins, margo, coin):
    indexes = {
        "usdt": 0,
        "wbtc": 1,
        "weth": 2,
    }
    i = indexes[coin]
    lp = "tricrypto2_lp"
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [i, 0, 4, 3, 3]
    amount = None if coin == "usdt" else 0.1
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["dai", "usdc", "usdt"])
def test_5(router, coins, margo, coin):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin]
    lp = "aave_lp"
    pool = "0xdebf20617708857ebe4f679508e7b7863a8a8eee"  # aave
    swap_params = [i, 0, 5, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["frax", "usdc"])
def test_6_stable_2coins_fraxusdc(router, coins, margo, coin):
    j = 0 if coin == "frax" else 1
    lp = "fraxbp"
    pool = "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2"  # fraxusdc
    swap_params = [0, j, 6, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 1e-7
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["frax", "usdp"])
def test_6_stable_2coins_fraxusdp(router, coins, margo, coin):
    j = 0 if coin == "frax" else 1
    lp = "fraxusdp_lp"
    pool = "0xaE34574AC03A15cd58A92DC79De7B1A0800F1CE3"  # fraxusdp
    swap_params = [0, j, 6, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 1e-7
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["dai", "usdc", "usdt"])
def test_6_stable_3coins(router, coins, margo, coin):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    j = indexes[coin]
    lp = "3crv"
    pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [0, j, 6, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10
    assert abs(amount - required) / amount < 1e-7
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["weth", "cvx"])
def test_6_crypto(router, coins, margo, coin):
    indexes = {
        "weth": 0,
        "cvx": 1,
    }
    j = indexes[coin]
    lp = "cvxeth_lp"
    pool = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4"  # cvxeth
    swap_params = [0, j, 6, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["usdt", "wbtc", "weth"])
def test_6_tricrypto(router, coins, margo, coin):
    indexes = {
        "usdt": 0,
        "wbtc": 1,
        "weth": 2,
    }
    j = indexes[coin]
    lp = "tricrypto2_lp"
    pool = "0xd51a44d3fae010294c616388b506acda1bfaae46"  # tricrypto2
    swap_params = [0, j, 6, 3, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 2e-3
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin", ["dai", "usdc", "usdt"])
def test_7(router, coins, margo, coin):
    indexes = {
        "dai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    j = indexes[coin]
    lp = "aave_lp"
    pool = "0xdebf20617708857ebe4f679508e7b7863a8a8eee"  # aave
    swap_params = [0, j, 7, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6
    assert abs(amount - required) / amount < 1e-3
    assert _get_balance(coins[coin], router) == 1


@pytest.mark.parametrize("coin1", ["eth", "weth"])
@pytest.mark.parametrize("coin2", ["eth", "weth"])
def test_8_weth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["weth"]
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


def test_8_steth(router, coins, margo):
    coin1 = "eth"
    coin2 = "steth"
    pool = coins[coin2].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 10
    assert abs(amount - required) / amount < 1e-15
    assert 1 <= _get_balance(coins[coin2], router) <= 2


def test_8_frxeth(router, coins, margo):
    coin1 = "eth"
    coin2 = "frxeth"
    pool = "0xbAFA44EFE7901E04E39Dad13167D089C559c1138"  # frxeth minter
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["steth", "wsteth"])
@pytest.mark.parametrize("coin2", ["steth", "wsteth"])
def test_8_wsteth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["wsteth"].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) <= 1
    assert abs((balances[1] - initial_balances[1]) - expected) <= 10
    assert abs(amount - required) / amount < 1e-15
    assert 1 <= _get_balance(coins[coin2], router) <= 2


@pytest.mark.parametrize("coin1", ["frxeth", "sfrxeth"])
@pytest.mark.parametrize("coin2", ["frxeth", "sfrxeth"])
def test_8_sfrxeth(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = coins["sfrxeth"].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


def test_8_wbeth(router, coins, margo):
    coin1 = "eth"
    coin2 = "wbeth"
    pool = coins[coin2].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


def test_8_susde(router, coins, margo):
    coin1 = "usde"
    coin2 = "susde"
    pool = coins[coin2].address
    swap_params = [0, 0, 8, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-6
    assert abs(amount - required) / amount < 1e-15
    assert _get_balance(coins[coin2], router) == 1


def test_route_2_steps(router, coins, margo):
    coin_names = ["eurt", "3crv", "dchf"]
    pools = [
        "0x9838eccc42659fa8aa7daf2ad134b53984c9427b",  # eurtusd
        "0xdcb11e81c8b8a1e06bf4b50d4f6f3bb31f7478c3",  # DCHF/3CRV (factory-crypto-116)
    ]
    swap_params = [[0, 1, 1, 2, 2], [1, 0, 1, 2, 2]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin_names[-1]], router) == 1


def test_route_2_steps_2(router, coins, margo):  # revert: NON_EMPTY_DATA
    coin_names = ["eth", "steth", "wsteth"]
    pools = [
        coins["steth"].address,
        coins["wsteth"].address,
    ]
    swap_params = [[0, 0, 8, 0, 0], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1
    assert abs(amount - required) <= 10
    assert _get_balance(coins[coin_names[-1]], router) == 1


def test_route_3_steps(router, coins, margo):
    coin_names = ["dai", "usdt", "eth", "wbeth"]
    pools = [
        "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7",  # 3pool
        "0xd51a44d3fae010294c616388b506acda1bfaae46",  # tricrypto2
        coins["wbeth"].address,
    ]
    swap_params = [[0, 2, 1, 1, 3], [0, 2, 1, 3, 3], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin_names[-1]], router) == 1


def test_route_4_steps(router, coins, margo):
    coin_names = ["dai", "usdt", "eth", "steth", "wsteth"]
    pools = [
        "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7",  # 3pool
        "0xd51a44d3fae010294c616388b506acda1bfaae46",  # tricrypto2
        "0xdc24316b9ae028f1497c275eb9192a3ea0f67022",  # steth
        coins["wsteth"].address,
    ]
    swap_params = [[0, 2, 1, 1, 3], [0, 2, 1, 3, 3], [0, 1, 1, 1, 2], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin_names[-1]], router) == 1


def test_route_5_steps(router, coins, margo):
    coin_names = ["3crv", "dai", "usdt", "eth", "steth", "wsteth"]
    pools = [
        "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7",  # 3pool
        "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7",  # 3pool
        "0xd51a44d3fae010294c616388b506acda1bfaae46",  # tricrypto2
        "0xdc24316b9ae028f1497c275eb9192a3ea0f67022",  # steth
        coins["wsteth"].address,
    ]
    swap_params = [[0, 0, 6, 1, 3], [0, 2, 1, 1, 3], [0, 2, 1, 3, 3], [0, 1, 1, 1, 2], [0, 0, 8, 0, 0]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin_names[-1]], router) == 1
