import pytest
from utils import _exchange, _get_balance

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


# ------------------------------- STABLE NG -------------------------------

@pytest.mark.parametrize("coin1", ["pyusd", "usdc"])
@pytest.mark.parametrize("coin2", ["pyusd", "usdc"])
def test_1_stable_ng(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    i, j = 0, 1
    if coin1 == "usdc":
        i, j = 1, 0
    pool = "0x383e6b4437b59fff47b619cba855ca29342a8559"  # PayPool (factory-stable-ng-43)
    swap_params = [i, j, 1, 10, 2]
    amount, expected, required, initial_balances, balances = _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 3e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdm", "3crv"])
@pytest.mark.parametrize("coin2", ["usdm", "3crv"])
def test_1_stable_ng_meta(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    i, j = 0, 1
    if coin1 == "3crv":
        i, j = 1, 0
    pool = "0xc83b79c07ece44b8b99ffa0e235c00add9124f9e"  # USDM-3crv (factory-stable-ng-26)
    swap_params = [i, j, 1, 10, 2]
    amount, expected, required, initial_balances, balances = _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert 0 <= balances[0] - (initial_balances[0] - amount) <= 1  # USDM is rebase token
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 1e-5
    assert 1 <= _get_balance(coins[coin2], router) <= 2  # USDM is rebase token


@pytest.mark.parametrize("coin1", ["mkusd", "paypool_lp"])
@pytest.mark.parametrize("coin2", ["mkusd", "paypool_lp"])
def test_1_stable_ng_meta_based_on_ng(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    i, j = 0, 1
    if coin1 == "paypool_lp":
        i, j = 1, 0
    pool = "0x9e10f9fb6f0d32b350cee2618662243d4f24c64a"  # mkUSD/Paypool (factory-stable-ng-91)
    swap_params = [i, j, 1, 10, 2]
    amount, expected, required, initial_balances, balances = _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin1", ["usdm", "dai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["usdm", "dai", "usdc", "usdt"])
def test_2_stable_ng_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "usdm": 0,
        "dai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xc83b79c07ece44b8b99ffa0e235c00add9124f9e"  # USDM-3crv (factory-stable-ng-26)
    base_pool = "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"  # 3pool
    swap_params = [i, j, 2, 10, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["3crv"].address)

    assert 0 <= balances[0] - (initial_balances[0] - amount) <= 1  # USDM is rebase token
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 2e-4
    assert 1 <= _get_balance(coins[coin2], router) <= 2  # USDM is rebase token


@pytest.mark.parametrize("coin1", ["mkusd", "pyusd", "usdc"])
@pytest.mark.parametrize("coin2", ["mkusd", "pyusd", "usdc"])
def test_2_stable_ng_meta_based_on_ng(router, coins, margo, coin1, coin2):
    indexes = {
        "mkusd": 0,
        "pyusd": 1,
        "usdc": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x9e10f9fb6f0d32b350cee2618662243d4f24c64a"  # mkUSD/Paypool (factory-stable-ng-91)
    base_pool = "0x383e6b4437b59fff47b619cba855ca29342a8559"  # PayPool
    swap_params = [i, j, 2, 10, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["paypool_lp"].address)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 3e-4
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin", ["pyusd", "usdc"])
def test_4_stable_ng(router, coins, margo, coin):
    i = 0 if coin == "pyusd" else 1
    pool = "0x383e6b4437b59fff47b619cba855ca29342a8559"  # PayPool (factory-stable-ng-43)
    lp = "paypool_lp"
    swap_params = [i, 0, 4, 10, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 2e-4
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["pyusd", "usdc"])
def test_6_stable_ng(router, coins, margo, coin):
    j = 0 if coin == "pyusd" else 1
    pool = "0x383e6b4437b59fff47b619cba855ca29342a8559"  # PayPool (factory-stable-ng-43)
    lp = "paypool_lp"
    swap_params = [0, j, 6, 10, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 2
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin], router) == 1


# ------------------------------- TWOCRYPTO NG -------------------------------

@pytest.mark.parametrize("coin1", ["weth", "cvg"])
@pytest.mark.parametrize("coin2", ["weth", "cvg"])
def test_1_twocrypto_ng(router, coins, margo, coin1, coin2):
    indexes = {
        "weth": 0,
        "cvg": 1
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x004c167d27ada24305b76d80762997fa6eb8d9b2"  # cvgeth
    swap_params = [i, j, 1, 20, 2]
    amount, expected, required, initial_balances, balances = _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin", ["weth", "cvg"])
def test_4_twocrypto_ng(router, coins, margo, coin):
    indexes = {
        "weth": 0,
        "cvg": 1
    }
    i = indexes[coin]
    lp = "cvgeth_lp"
    pool = "0x004c167d27ada24305b76d80762997fa6eb8d9b2"  # cvgeth
    swap_params = [i, 0, 4, 20, 2]
    amount = None if coin != "weth" else 0.1
    _exchange(router, coins, margo, [lp, "weth"], pool, [0, 0, 6, 20, 2], amount=1)  # needed to claim fees and make calculations precise
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["weth", "cvg"])
def test_6_twocrypto_ng(router, coins, margo, coin):
    indexes = {
        "weth": 0,
        "cvg": 1
    }
    j = indexes[coin]
    lp = "cvgeth_lp"
    pool = "0x004c167d27ada24305b76d80762997fa6eb8d9b2"  # cvgeth
    swap_params = [0, j, 6, 20, 2]
    amount = None if coin != "weth" else 0.1
    _exchange(router, coins, margo, [lp, coin], pool, swap_params, amount=1)  # needed to claim fees and make calculations precise
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) <= 1
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[coin], router) == 1


# ------------------------------- TRICRYPTO NG -------------------------------

@pytest.mark.parametrize("coin1", ["usdc", "wbtc", "eth", "weth"])
@pytest.mark.parametrize("coin2", ["usdc", "wbtc", "eth", "weth"])
def test_1_tricrypto_ng(router, coins, margo, coin1, coin2):
    indexes = {
        "usdc": 0,
        "wbtc": 1,
        "eth": 2,
        "weth": 2
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7f86bf177dd4f3494b841a37e810a34dd56c829b"  # TricryptoUSDC
    swap_params = [i, j, 1, 30, 3]
    amount = None if coin1 == "usdc" else 1
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 2e-5
    assert _get_balance(coins[coin2], router) == 1


@pytest.mark.parametrize("coin", ["usdc", "wbtc", "eth", "weth"])
def test_4_tricrypto_ng(router, coins, margo, coin):
    indexes = {
        "usdc": 0,
        "wbtc": 1,
        "eth": 2,
        "weth": 2
    }
    i = indexes[coin]
    lp = "tricryptousdc_lp"
    pool = "0x7f86bf177dd4f3494b841a37e810a34dd56c829b"  # TricryptoUSDC
    swap_params = [i, 0, 4, 30, 3]
    amount = None if coin == "usdc" else 1
    _exchange(router, coins, margo, [lp, "usdc"], pool, [0, 0, 6, 3, 3], amount=1)  # needed to claim fees and make calculations precise
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params, amount=amount)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[lp], router) == 1


@pytest.mark.parametrize("coin", ["usdc", "wbtc", "eth", "weth"])
def test_6_tricrypto_ng(router, coins, margo, coin):
    indexes = {
        "usdc": 0,
        "wbtc": 1,
        "eth": 2,
        "weth": 2
    }
    j = indexes[coin]
    lp = "tricryptousdc_lp"
    pool = "0x7f86bf177dd4f3494b841a37e810a34dd56c829b"  # TricryptoUSDC
    swap_params = [0, j, 6, 30, 3]
    _exchange(router, coins, margo, [lp, coin], pool, swap_params, amount=1)  # needed to claim fees and make calculations precise
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-8
    assert abs(amount - required) / amount < 1e-2
    assert _get_balance(coins[coin], router) == 1
