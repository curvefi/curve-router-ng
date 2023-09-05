import brownie
from brownie import ZERO_ADDRESS, ETH_ADDRESS

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
