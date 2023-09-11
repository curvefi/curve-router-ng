import datetime
import brownie
from brownie import ZERO_ADDRESS, ETH_ADDRESS, chain


MAX_STEPS = 5
ROUTE_LENGTH = MAX_STEPS * 2 + 1


def _is_weekend():
    n = datetime.datetime.today().weekday()

    if n < 5:
        return False
    else:  # 5 Sat, 6 Sun
        return True


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


def _exchange(router, coins, margo, coin_names, pools, _swap_params,
              amount=None, zaps=None, lp_tokens=None, base_pools=None, base_tokens=None, second_base_pools=None,
              second_base_tokens=None, test_slippage=True):
    if type(pools) != list:
        pools = [pools]
    if type(_swap_params[0]) != list:
        _swap_params = [_swap_params]
    if type(zaps) != list:
        zaps = list(filter(lambda x: x is not None, [zaps]))
    if type(lp_tokens) != list:
        lp_tokens = list(filter(lambda x: x is not None, [lp_tokens]))
    if type(base_pools) != list:
        base_pools = list(filter(lambda x: x is not None, [base_pools]))
    if type(base_tokens) != list:
        base_tokens = list(filter(lambda x: x is not None, [base_tokens]))
    if type(second_base_pools) != list:
        second_base_pools = list(filter(lambda x: x is not None, [second_base_pools]))
    if type(second_base_tokens) != list:
        second_base_tokens = list(filter(lambda x: x is not None, [second_base_tokens]))

    from_coin = coins[coin_names[0]]
    to_coin = coins[coin_names[-1]]
    zaps = _format_pools(zaps)
    lp_tokens = _format_pools(lp_tokens)

    route = []
    for i in range(len(pools)):
        coin2 = coins[coin_names[i + 1]]
        if i == 0:
            route += [from_coin, zaps[i], coin2] if zaps[i] != ZERO_ADDRESS else [from_coin, pools[i], coin2]
        else:
            route += [zaps[i], coin2] if zaps[i] != ZERO_ADDRESS else [pools[i], coin2]
    route = _format_route(route)
    swap_params = _format_swap_params(_swap_params)
    pools = _format_pools(pools)
    for i in range(len(pools)):
        if lp_tokens[i] != ZERO_ADDRESS:
            pools[i] = lp_tokens[i]  # for stablepools with swap_type = 4,5,6,7
    base_pools = _format_pools(base_pools)
    base_tokens = _format_pools(base_tokens)
    second_base_pools = _format_pools(second_base_pools)
    second_base_tokens = _format_pools(second_base_tokens)
    amount = (amount or 100) * 10**_get_decimals(from_coin)
    value = amount if from_coin == ETH_ADDRESS else 0

    initial_balances = [_get_balance(from_coin, margo), _get_balance(to_coin, margo)]
    expected = router.get_dy(route, swap_params, amount, pools)
    if chain.id == 137:
        required = router.get_dx(route, swap_params, expected, pools, base_pools, base_tokens, second_base_pools, second_base_tokens)
    else:
        required = router.get_dx(route, swap_params, expected, pools, base_pools, base_tokens)
    router.exchange(route, swap_params, amount, expected * 999 // 1000, pools, {"from": margo, "value": value})
    if test_slippage:
        with brownie.reverts("Slippage"):
            router.exchange(route, swap_params, amount, expected * 1001 // 1000, pools, {"from": margo, "value": value})
    balances = [_get_balance(from_coin, margo), _get_balance(to_coin, margo)]

    return amount, expected, required, initial_balances, balances
