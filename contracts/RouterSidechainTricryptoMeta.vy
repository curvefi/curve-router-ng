# @version 0.3.7
"""
@title Curve Registry Exchange Contract
@license MIT
@author Curve.Fi
@notice Find pools, query exchange rates and perform swaps
"""

from vyper.interfaces import ERC20

interface StablePool:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): payable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256): payable
    def get_dy(i: int128, j: int128, amount: uint256) -> uint256: view
    def get_dy_underlying(i: int128, j: int128, amount: uint256) -> uint256: view
    def coins(i: uint256) -> address: view
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256): nonpayable

interface CryptoPool:
    def exchange(i: uint256, j: uint256, dx: uint256, min_dy: uint256): payable
    def exchange_underlying(i: uint256, j: uint256, dx: uint256, min_dy: uint256): payable
    def get_dy(i: uint256, j: uint256, amount: uint256) -> uint256: view
    def get_dy_underlying(i: uint256, j: uint256, amount: uint256) -> uint256: view
    def calc_withdraw_one_coin(token_amount: uint256, i: uint256) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: uint256, min_amount: uint256): nonpayable

interface CryptoPoolETH:
    def exchange(i: uint256, j: uint256, dx: uint256, min_dy: uint256, use_eth: bool): payable

interface LendingBasePoolMetaZap:
    def exchange_underlying(pool: address, i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

interface CryptoMetaZap:
    def get_dy(pool: address, i: uint256, j: uint256, dx: uint256) -> uint256: view
    def exchange(pool: address, i: uint256, j: uint256, dx: uint256, min_dy: uint256, use_eth: bool): payable

interface StablePool2Coins:
    def add_liquidity(amounts: uint256[2], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[2], is_deposit: bool) -> uint256: view

interface CryptoPool2Coins:
    def calc_token_amount(amounts: uint256[2]) -> uint256: view

interface StablePool3Coins:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[3], is_deposit: bool) -> uint256: view

interface CryptoPool3Coins:
    def calc_token_amount(amounts: uint256[3]) -> uint256: view

interface StablePool4Coins:
    def add_liquidity(amounts: uint256[4], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[4], is_deposit: bool) -> uint256: view

interface CryptoPool4Coins:
    def calc_token_amount(amounts: uint256[4]) -> uint256: view

interface StablePool5Coins:
    def add_liquidity(amounts: uint256[5], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[5], is_deposit: bool) -> uint256: view

interface CryptoPool5Coins:
    def calc_token_amount(amounts: uint256[5]) -> uint256: view

interface LendingStablePool3Coins:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256, use_underlying: bool): nonpayable
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256, use_underlying: bool) -> uint256: nonpayable

interface Llamma:
    def get_dx(i: uint256, j: uint256, out_amount: uint256) -> uint256: view

interface WETH:
    def deposit(): payable
    def withdraw(_amount: uint256): nonpayable

interface stETH:
    def submit(_refferer: address): payable

interface frxETHMinter:
    def submit(): payable

interface wstETH:
    def getWstETHByStETH(_stETHAmount: uint256) -> uint256: view
    def getStETHByWstETH(_wstETHAmount: uint256) -> uint256: view
    def wrap(_stETHAmount: uint256) -> uint256: nonpayable
    def unwrap(_wstETHAmount: uint256) -> uint256: nonpayable

interface sfrxETH:
    def convertToShares(assets: uint256) -> uint256: view
    def convertToAssets(shares: uint256) -> uint256: view
    def deposit(assets: uint256, receiver: address) -> uint256: nonpayable
    def redeem(shares: uint256, receiver: address, owner: address) -> uint256: nonpayable

interface wBETH:
    def deposit(referral: address): payable
    def exchangeRate() -> uint256: view

# SNX
interface Synthetix:
    def exchangeAtomically(sourceCurrencyKey: bytes32, sourceAmount: uint256, destinationCurrencyKey: bytes32, trackingCode: bytes32, minAmount: uint256) -> uint256: nonpayable

interface SynthetixExchanger:
    def getAmountsForAtomicExchange(sourceAmount: uint256, sourceCurrencyKey: bytes32, destinationCurrencyKey: bytes32) -> AtomicAmountAndFee: view

interface SynthetixAddressResolver:
    def getAddress(name: bytes32) -> address: view

# Calc zaps
interface StableCalc:
    def calc_token_amount(pool: address, token: address, amounts: uint256[10], n_coins: uint256, deposit: bool, use_underlying: bool) -> uint256: view
    def get_dx(pool: address, i: int128, j: int128, dy: uint256, n_coins: uint256) -> uint256: view
    def get_dx_underlying(pool: address, i: int128, j: int128, dy: uint256, n_coins: uint256) -> uint256: view
    def get_dx_meta(pool: address, i: int128, j: int128, dy: uint256, n_coins: uint256, base_pool: address) -> uint256: view
    def get_dx_meta_underlying(pool: address, i: int128, j: int128, dy: uint256, n_coins: uint256, base_pool: address, base_token: address) -> uint256: view

interface CryptoCalc:
    def get_dx(pool: address, i: uint256, j: uint256, dy: uint256, n_coins: uint256) -> uint256: view
    def get_dx_meta_underlying(pool: address, i: uint256, j: uint256, dy: uint256, n_coins: uint256, base_pool: address, base_token: address) -> uint256: view
    def get_dx_tricrypto_meta_underlying(pool: address, i: uint256, j: uint256, dy: uint256, n_coins: uint256, base_pool: address, base_token: address) -> uint256: view
    def get_dx_double_meta_underlying(pool: address, i: uint256, j: uint256, dy: uint256, base_pool: address, base_pool_zap: address, base_pool2: address, base_token2: address) -> uint256: view


struct AtomicAmountAndFee:
    amountReceived: uint256
    fee: uint256
    exchangeFeeRate: uint256


event Exchange:
    sender: indexed(address)
    receiver: indexed(address)
    route: address[9]
    swap_params: uint256[5][4]
    pools: address[4]
    in_amount: uint256
    out_amount: uint256


ETH_ADDRESS: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
WETH_ADDRESS: immutable(address)

# Calc zaps
STABLE_CALC: immutable(StableCalc)
CRYPTO_CALC: immutable(CryptoCalc)

is_approved: HashMap[address, HashMap[address, bool]]
is_tricrypto_meta: HashMap[address, bool]


@external
@payable
def __default__():
    pass


@external
def __init__( _weth: address, _stable_calc: address, _crypto_calc: address, _tricrypto_meta_pools: address[2]):
    WETH_ADDRESS = _weth
    STABLE_CALC = StableCalc(_stable_calc)
    CRYPTO_CALC = CryptoCalc(_crypto_calc)

    if _tricrypto_meta_pools[0] != ZERO_ADDRESS:
        self.is_tricrypto_meta[_tricrypto_meta_pools[0]] = True
    if _tricrypto_meta_pools[1] != ZERO_ADDRESS:
        self.is_tricrypto_meta[_tricrypto_meta_pools[1]] = True


@external
@payable
def exchange(
    _route: address[9],
    _swap_params: uint256[5][4],
    _amount: uint256,
    _expected: uint256,
    _pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
    _receiver: address=msg.sender
) -> uint256:
    """
    @notice Performs up to 4 swaps in a single transaction.
    @dev Routing and swap params must be determined off-chain. This
         functionality is designed for gas efficiency over ease-of-use.
    @param _route Array of [initial token, pool or zap, token, pool or zap, token, ...]
                  The array is iterated until a pool address of 0x00, then the last
                  given token is transferred to `_receiver`
    @param _swap_params Multidimensional array of [i, j, swap type, pool_type, n_coins] where
                        i is the index of input token
                        j is the index of output token

                        The swap_type should be:
                        1. for `exchange`,
                        2. for `exchange_underlying`,
                        3. for underlying exchange via zap: factory stable metapools with lending base pool `exchange_underlying`
                           and factory crypto-meta pools underlying exchange (`exchange` method in zap)
                        4. for coin -> LP token "exchange" (actually `add_liquidity`),
                        5. for lending pool underlying coin -> LP token "exchange" (actually `add_liquidity`),
                        6. for LP token -> coin "exchange" (actually `remove_liquidity_one_coin`)
                        7. for LP token -> lending or fake pool underlying coin "exchange" (actually `remove_liquidity_one_coin`)
                        8. for ETH <-> WETH, ETH -> stETH or ETH -> frxETH, stETH <-> wstETH, frxETH <-> sfrxETH, ETH -> wBETH

                        pool_type: 1 - stable, 2 - crypto, 3 - tricrypto, 4 - llamma
                        n_coins is the number of coins in pool
    @param _amount The amount of input token (`_route[0]`) to be sent.
    @param _expected The minimum amount received after the final swap.
    @param _pools Array of pools for swaps via zap contracts. This parameter is only needed for swap_type = 3
    @param _receiver Address to transfer the final output token to.
    @return Received amount of the final output token.
    """
    input_token: address = _route[0]
    output_token: address = ZERO_ADDRESS
    amount: uint256 = _amount

    # validate / transfer initial token
    if input_token == ETH_ADDRESS:
        assert msg.value == amount
    else:
        assert msg.value == 0
        response: Bytes[32] = raw_call(
            input_token,
            _abi_encode(
                msg.sender,
                self,
                amount,
                method_id=method_id("transferFrom(address,address,uint256)"),
            ),
            max_outsize=32,
        )
        if len(response) != 0:
            assert convert(response, bool)

    for i in range(1, 5):
        # 4 rounds of iteration to perform up to 4 swaps
        swap: address = _route[i*2-1]
        pool: address = _pools[i-1] # Only for Polygon meta-factories underlying swap (swap_type == 6)
        output_token = _route[i*2]
        params: uint256[5] = _swap_params[i-1]  # i, j, swap_type, pool_type, n_coins

        if not self.is_approved[input_token][swap] and params[2] != 18:
            # approve the pool to transfer the input token
            response: Bytes[32] = raw_call(
                input_token,
                _abi_encode(
                    swap,
                    MAX_UINT256,
                    method_id=method_id("approve(address,uint256)"),
                ),
                max_outsize=32,
            )
            if len(response) != 0:  # For ETH
                assert convert(response, bool)
            self.is_approved[input_token][swap] = True

        eth_amount: uint256 = 0
        if input_token == ETH_ADDRESS:
            eth_amount = amount
        # perform the swap according to the swap type
        if params[2] == 1:
            if params[3] == 1:  # stable
                StablePool(swap).exchange(convert(params[0], int128), convert(params[1], int128), amount, 0, value=eth_amount)
            else:  # crypto, tricrypto or llamma
                if input_token == ETH_ADDRESS or output_token == ETH_ADDRESS:
                    CryptoPoolETH(swap).exchange(params[0], params[1], amount, 0, True, value=eth_amount)
                else:
                    CryptoPool(swap).exchange(params[0], params[1], amount, 0)
        elif params[2] == 2:
            if params[3] == 1:  # stable
                StablePool(swap).exchange_underlying(convert(params[0], int128), convert(params[1], int128), amount, 0, value=eth_amount)
            else:  # crypto or tricrypto
                CryptoPool(swap).exchange_underlying(params[0], params[1], amount, 0, value=eth_amount)
        elif params[2] == 3:  # swap is zap here
            if params[3] == 1:  # stable
                LendingBasePoolMetaZap(swap).exchange_underlying(pool, convert(params[0], int128), convert(params[1], int128), amount, 0)
            else:  # crypto or tricrypto
                use_eth: bool = input_token == ETH_ADDRESS or output_token == ETH_ADDRESS
                CryptoMetaZap(swap).exchange(pool, params[0], params[1], amount, 0, use_eth, value=eth_amount)
        elif params[2] == 4:
            if params[4] == 2:
                _amounts: uint256[2] = [0, 0]
                _amounts[params[0]] = amount
                StablePool2Coins(swap).add_liquidity(_amounts, 0)
            elif params[4] == 3:
                _amounts: uint256[3] = [0, 0, 0]
                _amounts[params[0]] = amount
                StablePool3Coins(swap).add_liquidity(_amounts, 0)
            elif params[4] == 4:
                _amounts: uint256[4] = [0, 0, 0, 0]
                _amounts[params[0]] = amount
                StablePool4Coins(swap).add_liquidity(_amounts, 0)
            elif params[4] == 5:
                _amounts: uint256[5] = [0, 0, 0, 0, 0]
                _amounts[params[0]] = amount
                StablePool5Coins(swap).add_liquidity(_amounts, 0)
        elif params[2] == 5:
            _amounts: uint256[3] = [0, 0, 0]
            _amounts[params[0]] = amount
            LendingStablePool3Coins(swap).add_liquidity(_amounts, 0, True) # example: aave on Polygon
        elif params[2] == 6:
            # The number of coins doesn't matter here
            if params[3] == 1:  # stable
                StablePool(swap).remove_liquidity_one_coin(amount, convert(params[1], int128), 0)
            else:  # crypto or tricrypto
                CryptoPool(swap).remove_liquidity_one_coin(amount, params[1], 0)  # example: atricrypto3 on Polygon
        elif params[2] == 7:
            # The number of coins doesn't matter here
            LendingStablePool3Coins(swap).remove_liquidity_one_coin(amount, convert(params[1], int128), 0, True) # example: aave on Polygon
        elif params[2] == 8:
            if input_token == ETH_ADDRESS and output_token == WETH_ADDRESS:
                WETH(swap).deposit(value=amount)
            elif input_token == WETH_ADDRESS and output_token == ETH_ADDRESS:
                WETH(swap).withdraw(amount)
            else:
                raise "Swap type 8 is only for ETH <-> WETH"
        else:
            raise "Bad swap type"

        # update the amount received
        if output_token == ETH_ADDRESS:
            amount = self.balance
        else:
            amount = ERC20(output_token).balanceOf(self)

        # sanity check, if the routing data is incorrect we will have a 0 balance and that is bad
        assert amount != 0, "Received nothing"

        # check if this was the last swap
        if i == 4 or _route[i*2+1] == ZERO_ADDRESS:
            break
        # if there is another swap, the output token becomes the input for the next round
        input_token = output_token

    amount -= 1  # Change non-zero -> non-zero costs less gas than zero -> non-zero
    assert amount >= _expected, "Slippage"

    # transfer the final token to the receiver
    if output_token == ETH_ADDRESS:
        raw_call(_receiver, b"", value=amount)
    else:
        response: Bytes[32] = raw_call(
            output_token,
            _abi_encode(
                _receiver,
                amount,
                method_id=method_id("transfer(address,uint256)"),
            ),
            max_outsize=32,
        )
        if len(response) != 0:
            assert convert(response, bool)

    log Exchange(msg.sender, _receiver, _route, _swap_params, _pools, _amount, amount)

    return amount


@view
@external
def get_dy(
    _route: address[9],
    _swap_params: uint256[5][4],
    _amount: uint256,
    _pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS]
) -> uint256:
    """
    @notice Get amount of the final output token received in an exchange
    @dev Routing and swap params must be determined off-chain. This
         functionality is designed for gas efficiency over ease-of-use.
    @param _route Array of [initial token, pool or zap, token, pool or zap, token, ...]
                  The array is iterated until a pool address of 0x00, then the last
                  given token is transferred to `_receiver`
    @param _swap_params Multidimensional array of [i, j, swap type, pool_type, n_coins] where
                        i is the index of input token
                        j is the index of output token

                        The swap_type should be:
                        1. for `exchange`,
                        2. for `exchange_underlying`,
                        3. for underlying exchange via zap: factory stable metapools with lending base pool `exchange_underlying`
                           and factory crypto-meta pools underlying exchange (`exchange` method in zap)
                        4. for coin -> LP token "exchange" (actually `add_liquidity`),
                        5. for lending pool underlying coin -> LP token "exchange" (actually `add_liquidity`),
                        6. for LP token -> coin "exchange" (actually `remove_liquidity_one_coin`)
                        7. for LP token -> lending or fake pool underlying coin "exchange" (actually `remove_liquidity_one_coin`)
                        8. for ETH <-> WETH, ETH -> stETH or ETH -> frxETH, stETH <-> wstETH, frxETH <-> sfrxETH, ETH -> wBETH

                        pool_type: 1 - stable, 2 - crypto, 3 - tricrypto, 4 - llamma
                        n_coins is the number of coins in pool
    @param _amount The amount of input token (`_route[0]`) to be sent.
    @param _pools Array of pools for swaps via zap contracts. This parameter is only needed for swap_type = 3
    @return Expected amount of the final output token.
    """
    input_token: address = _route[0]
    output_token: address = ZERO_ADDRESS
    amount: uint256 = _amount

    for i in range(1, 5):
        # 4 rounds of iteration to perform up to 4 swaps
        swap: address = _route[i*2-1]
        pool: address = _pools[i-1] # Only for Polygon meta-factories underlying swap (swap_type == 4)
        output_token = _route[i * 2]
        params: uint256[5] = _swap_params[i-1]  # i, j, swap_type, pool_type, n_coins

        # Calc output amount according to the swap type
        if params[2] == 1:
            if params[3] == 1:  # stable
                amount = StablePool(swap).get_dy(convert(params[0], int128), convert(params[1], int128), amount)
            else:  # crypto or llamma
                amount = CryptoPool(swap).get_dy(params[0], params[1], amount)
        elif params[2] == 2:
            if params[3] == 1:  # stable
                amount = StablePool(swap).get_dy_underlying(convert(params[0], int128), convert(params[1], int128), amount)
            else:  # crypto
                amount = CryptoPool(swap).get_dy_underlying(params[0], params[1], amount)
        elif params[2] == 3:  # swap is zap here
            if params[3] == 1:  # stable
                amount = StablePool(pool).get_dy_underlying(convert(params[0], int128), convert(params[1], int128), amount)
            else:  # crypto
                amount = CryptoMetaZap(swap).get_dy(pool, params[0], params[1], amount)
        elif params[2] in [4, 5]:
            # Some cryptopools have stablepool interface for calc_token_amount (tricrypto2 for example)
            if params[4] == 2:
                _amounts: uint256[2] = [0, 0]
                _amounts[params[0]] = amount
                if params[3] == 2:  # crypto
                    amount = CryptoPool2Coins(swap).calc_token_amount(_amounts)
                else:  # stable or tricrypto
                    amount = StablePool2Coins(swap).calc_token_amount(_amounts, True)
            elif params[4] == 3:
                _amounts: uint256[3] = [0, 0, 0]
                _amounts[params[0]] = amount
                if params[3] == 2:  # crypto
                    amount = CryptoPool3Coins(swap).calc_token_amount(_amounts)
                else:  # stable or tricrypto
                    amount = StablePool3Coins(swap).calc_token_amount(_amounts, True)
            elif params[4] == 4:
                _amounts: uint256[4] = [0, 0, 0, 0]
                _amounts[params[0]] = amount
                if params[3] == 2:  # crypto
                    amount = CryptoPool4Coins(swap).calc_token_amount(_amounts)
                else:  # stable or tricrypto
                    amount = StablePool4Coins(swap).calc_token_amount(_amounts, True)
            elif params[4] == 5:
                _amounts: uint256[5] = [0, 0, 0, 0, 0]
                _amounts[params[0]] = amount
                if params[3] == 2:  # crypto
                    amount = CryptoPool5Coins(swap).calc_token_amount(_amounts)
                else:  # stable or tricrypto
                    amount = StablePool5Coins(swap).calc_token_amount(_amounts, True)
        elif params[2] in [6, 7]:
            # The number of coins doesn't matter here
            if params[3] == 1:  # stable
                amount = StablePool(swap).calc_withdraw_one_coin(amount, convert(params[1], int128))
            else:  # crypto
                amount = CryptoPool(swap).calc_withdraw_one_coin(amount, params[1])
        elif params[2] == 8:
            if input_token == WETH_ADDRESS or output_token == WETH_ADDRESS:
                # ETH <--> WETH rate is 1:1
                pass
            else:
                raise "Swap type 8 is only for ETH <-> WETH"
        else:
            raise "Bad swap type"

        # check if this was the last swap
        if i == 4 or _route[i*2+1] == ZERO_ADDRESS:
            break
        # if there is another swap, the output token becomes the input for the next round
        input_token = output_token

    return amount - 1


@view
@external
def get_dx(
    _route: address[9],
    _swap_params: uint256[5][4],
    _out_amount: uint256,
    _pools: address[4],
    _base_pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
    _base_tokens: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
    _second_base_pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
    _second_base_tokens: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
) -> uint256:
    """
    @notice Calculate the input amount required to receive the desired output amount
    @dev Routing and swap params must be determined off-chain. This
         functionality is designed for gas efficiency over ease-of-use.
    @param _route Array of [initial token, pool or zap, token, pool or zap, token, ...]
                  The array is iterated until a pool address of 0x00, then the last
                  given token is transferred to `_receiver`
    @param _swap_params Multidimensional array of [i, j, swap type, pool_type, n_coins] where
                        i is the index of input token
                        j is the index of output token

                        The swap_type should be:
                        1. for `exchange`,
                        2. for `exchange_underlying`,
                        3. for underlying exchange via zap: factory stable metapools with lending base pool `exchange_underlying`
                           and factory crypto-meta pools underlying exchange (`exchange` method in zap)
                        4. for coin -> LP token "exchange" (actually `add_liquidity`),
                        5. for lending pool underlying coin -> LP token "exchange" (actually `add_liquidity`),
                        6. for LP token -> coin "exchange" (actually `remove_liquidity_one_coin`)
                        7. for LP token -> lending or fake pool underlying coin "exchange" (actually `remove_liquidity_one_coin`)
                        8. for ETH <-> WETH, ETH -> stETH or ETH -> frxETH, stETH <-> wstETH, frxETH <-> sfrxETH, ETH -> wBETH

                        pool_type: 1 - stable, 2 - crypto, 3 - tricrypto, 4 - llamma
                        n_coins is the number of coins in pool
    @param _out_amount The desired amount of output coin to receive.
    @param _pools Array of pools.
    @param _base_pools Array of base pools (for meta pools).
    @param _base_tokens Array of base lp tokens (for meta pools). Should be a zap address for double meta pools.
    @param _second_base_pools Array of the second base pools (for double meta pools like crv/tricrypto and wmatic/tricrypto).
    @param _second_base_tokens Array of the second base lp tokens (for double meta pools  like crv/tricrypto and wmatic/tricrypto).
    @return Required amount of input token to send.
    """
    input_token: address = _route[0]
    output_token: address = ZERO_ADDRESS
    amount: uint256 = _out_amount

    for _i in range(1, 5):
        # 4 rounds of iteration to perform up to 4 swaps
        i: uint256 = 5 - _i
        swap: address = _route[i*2-1]
        if swap == ZERO_ADDRESS:
            continue
        pool: address = _pools[i-1]
        base_pool: address = _base_pools[i-1]
        base_token: address = _base_tokens[i-1]
        second_base_pool: address = _second_base_pools[i-1]
        second_base_token: address = _second_base_tokens[i-1]
        output_token = _route[i * 2]
        params: uint256[5] = _swap_params[i-1]  # i, j, swap_type, n_coins, pool_type
        pool_type: uint256 = params[3]
        n_coins: uint256 = params[4]


        # Calc a required input amount according to the swap type
        if params[2] == 1:
            if pool_type == 1:  # stable
                if base_pool == ZERO_ADDRESS:  # non-meta
                    amount = STABLE_CALC.get_dx(pool, convert(params[0], int128), convert(params[1], int128), amount, n_coins)
                else:
                    amount = STABLE_CALC.get_dx_meta(pool, convert(params[0], int128), convert(params[1], int128), amount, n_coins, base_pool)
            elif pool_type in [2, 3]:  # crypto or tricrypto
                amount = CRYPTO_CALC.get_dx(pool, params[0], params[1], amount, n_coins)
            else:  # llamma
                amount = Llamma(pool).get_dx(params[0], params[1], amount)
        elif params[2] in [2, 3]:
            if pool_type == 1:  # stable
                if base_pool == ZERO_ADDRESS:  # non-meta
                    amount = STABLE_CALC.get_dx_underlying(pool, convert(params[0], int128), convert(params[1], int128), amount, n_coins)
                else:
                    amount = STABLE_CALC.get_dx_meta_underlying(pool, convert(params[0], int128), convert(params[1], int128), amount, n_coins, base_pool, base_token)
            else:  # crypto
                if second_base_pool != ZERO_ADDRESS:  # double-meta, swap is zap here, base_token is base_pool_zap here
                    amount = CRYPTO_CALC.get_dx_double_meta_underlying(pool, params[0], params[1], amount, base_pool, base_token, second_base_pool, second_base_token)
                elif self.is_tricrypto_meta[pool]:
                    amount = CRYPTO_CALC.get_dx_tricrypto_meta_underlying(pool, params[0], params[1], amount, n_coins, base_pool, base_token)
                else:
                    amount = CRYPTO_CALC.get_dx_meta_underlying(pool, params[0], params[1], amount, n_coins, base_pool, base_token)
        elif params[2] in [4, 5]:
            # The number of coins doesn't matter here.
            # This is not correct. Should be something like calc_add_one_coin. But tests say that it's precise enough.
            if pool_type == 1:  # stable
                amount = StablePool(swap).calc_withdraw_one_coin(amount, convert(params[0], int128))
            else:  # crypto
                amount = CryptoPool(swap).calc_withdraw_one_coin(amount, params[0])
        elif params[2] in [6, 7]:
            # Some cryptopools have stablepool interface for calc_token_amount (tricrypto2 for example)
            if n_coins == 2:
                _amounts: uint256[2] = [0, 0]
                _amounts[params[1]] = amount
                if pool_type == 2:  # crypto
                    amount = CryptoPool2Coins(swap).calc_token_amount(_amounts)  # This is not correct.
                else:  # stable or tricrypto
                    amount = StablePool2Coins(swap).calc_token_amount(_amounts, False)
            elif n_coins == 3:
                _amounts: uint256[3] = [0, 0, 0]
                _amounts[params[1]] = amount
                if pool_type == 2:  # crypto
                    amount = CryptoPool3Coins(swap).calc_token_amount(_amounts)  # This is not correct.
                else:  # stable or tricrypto
                    amount = StablePool3Coins(swap).calc_token_amount(_amounts, False)
            elif n_coins == 4:
                _amounts: uint256[4] = [0, 0, 0, 0]
                _amounts[params[1]] = amount
                if pool_type == 2:  # crypto
                    amount = CryptoPool4Coins(swap).calc_token_amount(_amounts)  # This is not correct.
                else:  # stable or tricrypto
                    amount = StablePool4Coins(swap).calc_token_amount(_amounts, False)
            elif n_coins == 5:
                _amounts: uint256[5] = [0, 0, 0, 0, 0]
                _amounts[params[1]] = amount
                if pool_type == 2:  # crypto
                    amount = CryptoPool5Coins(swap).calc_token_amount(_amounts)  # This is not correct.
                else:  # stable or tricrypto
                    amount = StablePool5Coins(swap).calc_token_amount(_amounts, False)
        elif params[2] == 8:
            if input_token == WETH_ADDRESS or output_token == WETH_ADDRESS:
                # ETH <--> WETH rate is 1:1
                pass
            else:
                raise "Swap type 8 is only for ETH <-> WETH"
        else:
            raise "Bad swap type"

        # if there is another swap, the output token becomes the input for the next round
        input_token = output_token

    return amount