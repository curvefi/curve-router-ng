import pytest
from utils import _exchange, ZERO_ADDRESS

pytestmark = pytest.mark.usefixtures("mint_margo", "approve_margo")


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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params)

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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["am3crv"], amount=1)

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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=coins["am3crv"])

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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=base_pool_zap,
                  second_base_pools=second_base_pool, second_base_tokens=coins["am3crv"],
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
        _exchange(router, coins, margo, [coin1, coin2], pool, swap_params,
                  zaps=zap, base_pools=base_pool, base_tokens=base_pool_zap,
                  second_base_pools=second_base_pool, second_base_tokens=coins["am3crv"],
                  amount=1, test_slippage=False)

    assert initial_balances[0] - amount == balances[0]
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-3
    assert abs(amount - required) / amount < 1e-2


def test_route_2_steps(router, coins, margo):
    coin_names = ["amdai", "am3crv", "dai"]

    pools = [
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
    ]
    swap_params = [[0, 0, 4, 1, 3], [0, 0, 7, 1, 3]]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-6
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-3


def test_route_3_steps(router, coins, margo):
    coin_names = ["amdai", "am3crv", "dai", "crv"]

    pools = [
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0xc7c939a474cb10eb837894d1ed1a77c61b268fa7",  # crv/tricrypto
    ]
    swap_params = [[0, 0, 4, 1, 3], [0, 0, 7, 1, 3], [1, 0, 3, 2, 6]]
    zaps = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x3d8EADb739D1Ef95dd53D718e4810721837c69c1"  # atricrypto3 meta zap
    ]
    base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x92215849c439E1f8612b6646060B4E3E5ef822cC",  # atricrypto3
    ]
    base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8",  # atricrypto3 zap
    ]
    second_base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
    ]
    second_base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        coins["am3crv"],
    ]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  zaps=zaps, base_pools=base_pools, base_tokens=base_tokens,
                  second_base_pools=second_base_pools, second_base_tokens=second_base_tokens,
                  test_slippage=False)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-6
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-2


def test_route_4_steps(router, coins, margo):
    coin_names = ["amdai", "am3crv", "dai", "matic", "wmatic"]

    pools = [
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x7bbc0e92505b485aeb3e82e828cb505daf1e50c6",  # wmatic/tricrypto
        coins["wmatic"].address,
    ]
    swap_params = [[0, 0, 4, 1, 3], [0, 0, 7, 1, 3], [1, 0, 3, 2, 6], [0, 0, 8, 0, 0]]
    zaps = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x3d8EADb739D1Ef95dd53D718e4810721837c69c1"  # atricrypto3 meta zap
    ]
    base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x92215849c439E1f8612b6646060B4E3E5ef822cC",  # atricrypto3
    ]
    base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8",  # atricrypto3 zap
    ]
    second_base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
    ]
    second_base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        coins["am3crv"],
    ]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  zaps=zaps, base_pools=base_pools, base_tokens=base_tokens,
                  second_base_pools=second_base_pools, second_base_tokens=second_base_tokens,
                  test_slippage=False)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-6
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-2


def test_route_5_steps(router, coins, margo):
    coin_names = ["amusdt", "amdai", "am3crv", "dai", "matic", "wmatic"]

    pools = [
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
        "0x7bbc0e92505b485aeb3e82e828cb505daf1e50c6",  # wmatic/tricrypto
        coins["wmatic"].address,
    ]
    swap_params = [[2, 0, 1, 1, 3], [0, 0, 4, 1, 3], [0, 0, 7, 1, 3], [1, 0, 3, 2, 6], [0, 0, 8, 0, 0]]
    zaps = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x3d8EADb739D1Ef95dd53D718e4810721837c69c1"  # atricrypto3 meta zap
    ]
    base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x92215849c439E1f8612b6646060B4E3E5ef822cC",  # atricrypto3
    ]
    base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8",  # atricrypto3 zap
    ]
    second_base_pools = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        "0x445FE580eF8d70FF569aB36e80c647af338db351",  # aave
    ]
    second_base_tokens = [
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        coins["am3crv"],
    ]
    amount, expected, required, initial_balances, balances = \
        _exchange(router, coins, margo, coin_names, pools, swap_params,
                  zaps=zaps, base_pools=base_pools, base_tokens=base_tokens,
                  second_base_pools=second_base_pools, second_base_tokens=second_base_tokens,
                  test_slippage=False)

    assert abs((initial_balances[0] - amount) - balances[0]) / balances[0] < 1e-6
    assert abs((balances[1] - initial_balances[1]) - expected) / expected < 1e-7 or (balances[1] - initial_balances[1]) - expected <= 100
    assert abs(amount - required) / amount < 1e-2
