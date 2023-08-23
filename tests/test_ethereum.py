import pytest
from brownie import Contract, ZERO_ADDRESS
from brownie.test import given, strategy
from hypothesis import settings
from datetime import timedelta

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")

MAX_STEPS = 4
ROUTE_LENGTH = MAX_STEPS * 2 + 1


def format_route(route: list[str]) -> list[str]:
    return route + [ZERO_ADDRESS] * (ROUTE_LENGTH - len(route))


def format_swap_params(swap_params: list[list[int]]) -> list[list[int]]:
    return swap_params + [[0, 0, 0]] * (MAX_STEPS - len(swap_params))


@pytest.mark.parametrize("coin1_name", ["susd", "seur", "seth", "sbtc"])
@pytest.mark.parametrize("coin2_name", ["susd", "seur", "seth", "sbtc"])
def test_16(router, coins, margo, coin1_name, coin2_name):
    if coin1_name == coin2_name:
        return
    coin1 = coins[coin1_name]
    coin2 = coins[coin2_name]
    route = format_route([coin1.address, "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F", coin2.address])
    swap_params = format_swap_params([[0, 0, 16]])
    amount = 100 * 10**coin1.decimals()

    initial_balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]
    expected = router.get_dy(route, swap_params, amount)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, {"from": margo})
    balances = [coin1.balanceOf(margo), coin2.balanceOf(margo)]

    assert initial_balances[0] - amount == balances[0]
    assert balances[1] - initial_balances[1] == expected
