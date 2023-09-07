import pytest
from utils import _exchange

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


@pytest.mark.parametrize("coin1", ["wxdai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["wxdai", "usdc", "usdt"])
def test_1_stable(router, coins, margo, coin1, coin2):
    indexes = {
        "wxdai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["rai", "x3crv"])
@pytest.mark.parametrize("coin2", ["rai", "x3crv"])
def test_1_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "rai": 0,
        "x3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x85bA9Dfb4a3E4541420Fc75Be02E2B42042D7e46"  # rai
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["x3crv"])

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["eure", "x3crv"])
@pytest.mark.parametrize("coin2", ["eure", "x3crv"])
def test_1_crypto_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "eure": 0,
        "x3crv": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x056C6C5e684CeC248635eD86033378Cc444459B0"  # eureusd
    swap_params = [i, j, 1, 2, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["rai", "wxdai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["rai", "wxdai", "usdc", "usdt"])
def test_2_stable_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "rai": 0,
        "wxdai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x85bA9Dfb4a3E4541420Fc75Be02E2B42042D7e46"  # rai
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    swap_params = [i, j, 2, 1, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  base_pools=base_pool, base_tokens=coins["x3crv"], amount=1, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-4
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin1", ["eure", "wxdai", "usdc", "usdt"])
@pytest.mark.parametrize("coin2", ["eure", "wxdai", "usdc", "usdt"])
def test_2_crypto_meta(router, coins, margo, coin1, coin2):
    indexes = {
        "eure": 0,
        "wxdai": 1,
        "usdc": 2,
        "usdt": 3,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0x056C6C5e684CeC248635eD86033378Cc444459B0"  # eureusd
    base_pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    zap = "0xE3FFF29d4DC930EBb787FeCd49Ee5963DADf60b6"
    swap_params = [i, j, 2, 2, 4]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["x3crv"], test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin", ["wxdai", "usdc", "usdt"])
def test_4_stable(router, coins, margo, coin):
    indexes = {
        "wxdai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    i = indexes[coin]
    lp = "x3crv"
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    swap_params = [i, 0, 4, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin, lp], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


@pytest.mark.parametrize("coin", ["wxdai", "usdc", "usdt"])
def test_6_stable(router, coins, margo, coin):
    indexes = {
        "wxdai": 0,
        "usdc": 1,
        "usdt": 2,
    }
    j = indexes[coin]
    lp = "x3crv"
    pool = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"  # 3pool
    swap_params = [0, j, 6, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [lp, coin], pool, swap_params, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-3


def test_route_2_steps(router, coins, margo):
    coin_names = ["eure", "usdt", "rai"]

    pools = [
        "0x056C6C5e684CeC248635eD86033378Cc444459B0",  # eureusd
        "0x85bA9Dfb4a3E4541420Fc75Be02E2B42042D7e46",  # rai
    ]
    swap_params = [[0, 3, 2, 2, 4], [3, 0, 2, 1, 4]]
    zaps = [
        "0xE3FFF29d4DC930EBb787FeCd49Ee5963DADf60b6"
    ]
    base_pools = [
        "0x7f90122BF0700F9E7e1F688fe926940E8839F353",  # 3pool
        "0x7f90122BF0700F9E7e1F688fe926940E8839F353",  # 3pool
    ]
    base_tokens = [
        coins["x3crv"].address,
        coins["x3crv"].address,
    ]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  zaps=zaps, base_pools=base_pools, base_tokens=base_tokens, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7
    assert abs(amount - required) / amount < 1e-3
