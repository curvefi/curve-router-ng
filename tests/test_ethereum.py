import pytest
from brownie import ZERO_ADDRESS

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")

MAX_STEPS = 4
ROUTE_LENGTH = MAX_STEPS * 2 + 1


def format_route(route: list[str]) -> list[str]:
    return route + [ZERO_ADDRESS] * (ROUTE_LENGTH - len(route))


def format_swap_params(swap_params: list[list[int]]) -> list[list[int]]:
    return swap_params + [[0, 0, 0]] * (MAX_STEPS - len(swap_params))


def test_16_steth(router, coins, margo):
    coin1_name = "eth"
    coin2_name = "steth"
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1, coin2.address, coin2.address])
    swap_params = format_swap_params([[0, 0, 16]])
    amount = 100 * 10**18

    initial_balances = [margo.balance(), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo, "value": amount})
    balances = [margo.balance(), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert expected - (balances[1] - initial_balances[1]) <= 2


def test_16_frxeth(router, coins, margo):
    coin1_name = "eth"
    coin2_name = "frxeth"
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1, "0xbAFA44EFE7901E04E39Dad13167D089C559c1138", coin2.address])
    swap_params = format_swap_params([[0, 0, 16]])
    amount = 100 * 10**18

    initial_balances = [margo.balance(), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo, "value": amount})
    balances = [margo.balance(), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected


@pytest.mark.parametrize("coin1_name", ["steth", "wsteth"])
@pytest.mark.parametrize("coin2_name", ["steth", "wsteth"])
def test_17_wsteth(router, coins, margo, coin1_name, coin2_name):
    if coin1_name == coin2_name:
        return
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1.address, coins["wsteth"].address, coin2.address])
    swap_params = format_swap_params([[0, 0, 17]])
    amount = 100 * 10**coin1.decimals()

    initial_balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo})
    balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert expected - balances[1] - initial_balances[1] <= 2


@pytest.mark.parametrize("coin1_name", ["frxeth", "sfrxeth"])
@pytest.mark.parametrize("coin2_name", ["frxeth", "sfrxeth"])
def test_17_sfrxeth(router, coins, margo, coin1_name, coin2_name):
    if coin1_name == coin2_name:
        return
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1.address, coins["sfrxeth"].address, coin2.address])
    swap_params = format_swap_params([[0, 0, 17]])
    amount = 100 * 10**coin1.decimals()

    initial_balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo})
    balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7


@pytest.mark.parametrize("coin1_name", ["susd", "seur", "seth", "sbtc"])
@pytest.mark.parametrize("coin2_name", ["susd", "seur", "seth", "sbtc"])
def test_18(router, coins, margo, coin1_name, coin2_name):
    if coin1_name == coin2_name:
        return
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1.address, "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F", coin2.address])
    swap_params = format_swap_params([[0, 0, 18]])
    amount = 100 * 10**coin1.decimals()

    initial_balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo})
    balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
