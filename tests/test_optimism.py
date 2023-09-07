import pytest
from utils import _exchange

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
    pool = "0x1337BedC9D22ecbe766dF105c9623922A27963EC"  # 3pool
    swap_params = [i, j, 1, 1, 3]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["eth", "wsteth"])
@pytest.mark.parametrize("coin2", ["eth", "wsteth"])
def test_1_stable_eth(router, coins, margo, coin1, coin2):
    indexes = {
        "eth": 0,
        "wsteth": 1,
    }
    i = indexes[coin1]
    j = indexes[coin2]
    if i == j:
        return
    pool = "0xB90B9B1F91a01Ea22A182CD84C1E22222e39B415"  # wsteth
    swap_params = [i, j, 1, 1, 2]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-10 or (balances[1] - initial_balances[1]) - expected <= 100


@pytest.mark.parametrize("coin1", ["susd", "seur", "seth", "sbtc"])
@pytest.mark.parametrize("coin2", ["susd", "seur", "seth", "sbtc"])
def test_9(router, coins, margo, coin1, coin2):
    if coin1 == coin2:
        return
    pool = "0x8700dAec35aF8Ff88c16BdF0418774CB3D7599B4"  # SNX
    swap_params = [0, 0, 9, 0, 0]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params, amount=1, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
    assert abs(amount - required) / amount < 1e-9
