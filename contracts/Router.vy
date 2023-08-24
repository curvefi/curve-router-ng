# @version 0.3.7
"""
@title Curve Registry Exchange Contract
@license MIT
@author Curve.Fi
@notice Find pools, query exchange rates and perform swaps
"""

from vyper.interfaces import ERC20

interface CurvePool:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): payable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256): payable
    def get_dy(i: int128, j: int128, amount: uint256) -> uint256: view
    def get_dy_underlying(i: int128, j: int128, amount: uint256) -> uint256: view
    def coins(i: uint256) -> address: view

interface CryptoPool:
    def exchange(i: uint256, j: uint256, dx: uint256, min_dy: uint256): payable
    def exchange_underlying(i: uint256, j: uint256, dx: uint256, min_dy: uint256): payable
    def get_dy(i: uint256, j: uint256, amount: uint256) -> uint256: view
    def get_dy_underlying(i: uint256, j: uint256, amount: uint256) -> uint256: view

interface CryptoPoolETH:
    def exchange(i: uint256, j: uint256, dx: uint256, min_dy: uint256, use_eth: bool): payable

interface LendingBasePoolMetaZap:
    def exchange_underlying(pool: address, i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

interface CryptoMetaZap:
    def get_dy(pool: address, i: uint256, j: uint256, dx: uint256) -> uint256: view
    def exchange(pool: address, i: uint256, j: uint256, dx: uint256, min_dy: uint256, use_eth: bool): payable

interface BasePool2Coins:
    def add_liquidity(amounts: uint256[2], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[2], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256): nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view

interface BasePool3Coins:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[3], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256): nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view

interface LendingBasePool3Coins:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256, use_underlying: bool): nonpayable
    def calc_token_amount(amounts: uint256[3], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256, use_underlying: bool) -> uint256: nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view

interface CryptoBasePool3Coins:
    def add_liquidity(amounts: uint256[3], min_mint_amount: uint256, use_underlying: bool): nonpayable
    def calc_token_amount(amounts: uint256[3], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: uint256, min_amount: uint256): nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: uint256) -> uint256: view

interface BasePool4Coins:
    def add_liquidity(amounts: uint256[4], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[4], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256): nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view

interface BasePool5Coins:
    def add_liquidity(amounts: uint256[5], min_mint_amount: uint256): nonpayable
    def calc_token_amount(amounts: uint256[5], is_deposit: bool) -> uint256: view
    def remove_liquidity_one_coin(token_amount: uint256, i: int128, min_amount: uint256): nonpayable
    def calc_withdraw_one_coin(token_amount: uint256, i: int128) -> uint256: view

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

# SNX
interface Synthetix:
    def exchangeAtomically(sourceCurrencyKey: bytes32, sourceAmount: uint256, destinationCurrencyKey: bytes32, trackingCode: bytes32, minAmount: uint256) -> uint256: nonpayable

interface SynthetixExchanger:
    def getAmountsForAtomicExchange(sourceAmount: uint256, sourceCurrencyKey: bytes32, destinationCurrencyKey: bytes32) -> AtomicAmountAndFee: view

interface SynthetixAddressResolver:
    def getAddress(name: bytes32) -> address: view


struct AtomicAmountAndFee:
    amountReceived: uint256
    fee: uint256
    exchangeFeeRate: uint256


event ExchangeMultiple:
    buyer: indexed(address)
    receiver: indexed(address)
    route: address[9]
    swap_params: uint256[3][4]
    pools: address[4]
    amount_sold: uint256
    amount_bought: uint256

ETH_ADDRESS: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
STETH_ADDRESS: constant(address) = 0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84
FRXETH_ADDRESS: constant(address) = 0x5E8422345238F34275888049021821E8E08CAa1f

is_approved: HashMap[address, HashMap[address, bool]]

# SNX
SNX_ADDRESS_RESOLVER: constant(address) = 0x823bE81bbF96BEc0e25CA13170F5AaCb5B79ba83
SNX_TRACKING_CODE: constant(bytes32) = 0x4355525645000000000000000000000000000000000000000000000000000000
SNX_EXCHANGE_RATES_NAME: constant(bytes32) = 0x45786368616E6765720000000000000000000000000000000000000000000000
snx_currency_keys: HashMap[address, bytes32]


@external
@payable
def __default__():
    pass


@external
def __init__():
    self.snx_currency_keys[0x57Ab1ec28D129707052df4dF418D58a2D46d5f51] = 0x7355534400000000000000000000000000000000000000000000000000000000  # sUSD
    self.snx_currency_keys[0xD71eCFF9342A5Ced620049e616c5035F1dB98620] = 0x7345555200000000000000000000000000000000000000000000000000000000  # sEUR
    self.snx_currency_keys[0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6] = 0x7342544300000000000000000000000000000000000000000000000000000000  # sBTC
    self.snx_currency_keys[0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb] = 0x7345544800000000000000000000000000000000000000000000000000000000  # sETH

    self.is_approved[0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0][0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0] = True  # wstETH
    self.is_approved[0xac3E018457B222d93114458476f3E3416Abbe38F][0xac3E018457B222d93114458476f3E3416Abbe38F] = True  # sfrxETH

@external
@payable
def exchange(
    _route: address[9],
    _swap_params: uint256[3][4],
    _amount: uint256,
    _expected: uint256,
    _pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS],
    _receiver: address=msg.sender
) -> uint256:
    """
    @notice Perform up to four swaps in a single transaction
    @dev Routing and swap params must be determined off-chain. This
         functionality is designed for gas efficiency over ease-of-use.
    @param _route Array of [initial token, pool, token, pool, token, ...]
                  The array is iterated until a pool address of 0x00, then the last
                  given token is transferred to `_receiver`
    @param _swap_params Multidimensional array of [i, j, swap type] where i and j are the correct
                        values for the n'th pool in `_route`. The swap type should be
                        1 for a stableswap `exchange`,
                        2 for stableswap `exchange_underlying`,
                        3 for a cryptoswap `exchange`,
                        4 for a cryptoswap `exchange_underlying`,
                        5 for factory metapools with lending base pool `exchange_underlying`,
                        6 for factory crypto-meta pools underlying exchange (`exchange` method in zap),
                        7-11 for wrapped coin (underlying for lending or fake pool) -> LP token "exchange" (actually `add_liquidity`),
                        12-14 for LP token -> wrapped coin (underlying for lending pool) "exchange" (actually `remove_liquidity_one_coin`)
                        15 for WETH -> ETH "exchange" (actually deposit/withdraw)
    @param _amount The amount of `_route[0]` token being sent.
    @param _expected The minimum amount received after the final swap.
    @param _pools Array of pools for swaps via zap contracts. This parameter is only needed for
                  Polygon meta-factories underlying swaps.
    @param _receiver Address to transfer the final output token to.
    @return Received amount of the final output token
    """
    input_token: address = _route[0]
    amount: uint256 = _amount
    output_token: address = ZERO_ADDRESS

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

    for i in range(1,5):
        # 4 rounds of iteration to perform up to 4 swaps
        swap: address = _route[i*2-1]
        pool: address = _pools[i-1] # Only for Polygon meta-factories underlying swap (swap_type == 6)
        output_token = _route[i*2]
        params: uint256[3] = _swap_params[i-1]  # i, j, swap_type

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
            CurvePool(swap).exchange(convert(params[0], int128), convert(params[1], int128), amount, 0, value=eth_amount)
        elif params[2] == 2:
            CurvePool(swap).exchange_underlying(convert(params[0], int128), convert(params[1], int128), amount, 0, value=eth_amount)
        elif params[2] == 3:
            if input_token == ETH_ADDRESS or output_token == ETH_ADDRESS:
                CryptoPoolETH(swap).exchange(params[0], params[1], amount, 0, True, value=eth_amount)
            else:
                CryptoPool(swap).exchange(params[0], params[1], amount, 0)
        elif params[2] == 4:
            CryptoPool(swap).exchange_underlying(params[0], params[1], amount, 0, value=eth_amount)
        elif params[2] == 5:
            LendingBasePoolMetaZap(swap).exchange_underlying(pool, convert(params[0], int128), convert(params[1], int128), amount, 0)
        elif params[2] == 6:
            use_eth: bool = input_token == ETH_ADDRESS or output_token == ETH_ADDRESS
            CryptoMetaZap(swap).exchange(pool, params[0], params[1], amount, 0, use_eth, value=eth_amount)
        elif params[2] == 7:
            _amounts: uint256[2] = [0, 0]
            _amounts[params[0]] = amount
            BasePool2Coins(swap).add_liquidity(_amounts, 0)
        elif params[2] == 8:
            _amounts: uint256[3] = [0, 0, 0]
            _amounts[params[0]] = amount
            BasePool3Coins(swap).add_liquidity(_amounts, 0)
        elif params[2] == 9:
            _amounts: uint256[3] = [0, 0, 0]
            _amounts[params[0]] = amount
            LendingBasePool3Coins(swap).add_liquidity(_amounts, 0, True) # example: aave on Polygon
        elif params[2] == 10:
            _amounts: uint256[4] = [0, 0, 0, 0]
            _amounts[params[0]] = amount
            BasePool4Coins(swap).add_liquidity(_amounts, 0)
        elif params[2] == 11:
            _amounts: uint256[5] = [0, 0, 0, 0, 0]
            _amounts[params[0]] = amount
            BasePool5Coins(swap).add_liquidity(_amounts, 0)
        elif params[2] == 12:
            # The number of coins doesn't matter here
            BasePool3Coins(swap).remove_liquidity_one_coin(amount, convert(params[1], int128), 0)
        elif params[2] == 13:
            # The number of coins doesn't matter here
            LendingBasePool3Coins(swap).remove_liquidity_one_coin(amount, convert(params[1], int128), 0, True) # example: aave on Polygon
        elif params[2] == 14:
            # The number of coins doesn't matter here
            CryptoBasePool3Coins(swap).remove_liquidity_one_coin(amount, params[1], 0) # example: atricrypto3 on Polygon
        elif params[2] == 15:
            if input_token == ETH_ADDRESS:
                WETH(swap).deposit(value=amount)
            elif output_token == ETH_ADDRESS:
                WETH(swap).withdraw(amount)
            else:
                raise "One of the coins must be ETH for swap type 15"
        elif params[2] == 16:
            assert input_token == ETH_ADDRESS, "Input coin must be ETH for swap type 16"
            if output_token == STETH_ADDRESS:
                stETH(swap).submit(0x0000000000000000000000000000000000000000, value=amount)
            elif output_token == FRXETH_ADDRESS:
                frxETHMinter(swap).submit(value=amount)
            else:
                raise "Swap type 16 is for ETH -> stETH or ETH -> frxETH only"
        elif params[2] == 17:
            if input_token == STETH_ADDRESS:
                wstETH(swap).wrap(amount)
            elif output_token == STETH_ADDRESS:
                wstETH(swap).unwrap(amount)
            elif input_token == FRXETH_ADDRESS:
                sfrxETH(swap).deposit(amount, self)
            elif output_token == FRXETH_ADDRESS:
                sfrxETH(swap).redeem(amount, self, self)
            else:
                raise "Swap type 17 is for stETH <-> wstETH or frxETH <-> sfrxETH only"
        elif params[2] == 18:
            Synthetix(swap).exchangeAtomically(self.snx_currency_keys[input_token], amount, self.snx_currency_keys[output_token], SNX_TRACKING_CODE, 0)
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

    # validate the final amount received
    assert amount >= _expected

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

    log ExchangeMultiple(msg.sender, _receiver, _route, _swap_params, _pools, _amount, amount)

    return amount


@view
@external
def get_dy(
    _route: address[9],
    _swap_params: uint256[3][4],
    _amount: uint256,
    _pools: address[4]=[ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS]
) -> uint256:
    """
    @notice Get the current number the final output tokens received in an exchange
    @dev Routing and swap params must be determined off-chain. This
         functionality is designed for gas efficiency over ease-of-use.
    @param _route Array of [initial token, pool, token, pool, token, ...]
                  The array is iterated until a pool address of 0x00, then the last
                  given token is transferred to `_receiver`
    @param _swap_params Multidimensional array of [i, j, swap type] where i and j are the correct
                        values for the n'th pool in `_route`. The swap type should be
                        1 for a stableswap `exchange`,
                        2 for stableswap `exchange_underlying`,
                        3 for a cryptoswap `exchange`,
                        4 for a cryptoswap `exchange_underlying`,
                        5 for factory metapools with lending base pool `exchange_underlying`,
                        6 for factory crypto-meta pools underlying exchange (`exchange` method in zap),
                        7-11 for wrapped coin (underlying for lending pool) -> LP token "exchange" (actually `add_liquidity`),
                        12-14 for LP token -> wrapped coin (underlying for lending or fake pool) "exchange" (actually `remove_liquidity_one_coin`)
                        15 for WETH -> ETH "exchange" (actually deposit/withdraw)
    @param _amount The amount of `_route[0]` token to be sent.
    @param _pools Array of pools for swaps via zap contracts. This parameter is only needed for
                  Polygon meta-factories underlying swaps.
    @return Expected amount of the final output token
    """
    input_token: address = _route[0]
    amount: uint256 = _amount
    output_token: address = ZERO_ADDRESS

    for i in range(1,5):
        # 4 rounds of iteration to perform up to 4 swaps
        swap: address = _route[i*2-1]
        pool: address = _pools[i-1] # Only for Polygon meta-factories underlying swap (swap_type == 4)
        output_token = _route[i * 2]
        params: uint256[3] = _swap_params[i-1]  # i, j, swap type

        # Calc output amount according to the swap type
        if params[2] == 1:
            amount = CurvePool(swap).get_dy(convert(params[0], int128), convert(params[1], int128), amount)
        elif params[2] == 2:
            amount = CurvePool(swap).get_dy_underlying(convert(params[0], int128), convert(params[1], int128), amount)
        elif params[2] == 3:
            amount = CryptoPool(swap).get_dy(params[0], params[1], amount)
        elif params[2] == 4:
            amount = CryptoPool(swap).get_dy_underlying(params[0], params[1], amount)
        elif params[2] == 5:
            amount = CurvePool(pool).get_dy_underlying(convert(params[0], int128), convert(params[1], int128), amount)
        elif params[2] == 6:
            amount = CryptoMetaZap(swap).get_dy(pool, params[0], params[1], amount)
        elif params[2] == 7:
            _amounts: uint256[2] = [0, 0]
            _amounts[params[0]] = amount
            amount = BasePool2Coins(swap).calc_token_amount(_amounts, True)
        elif params[2] in [8, 9]:
            _amounts: uint256[3] = [0, 0, 0]
            _amounts[params[0]] = amount
            amount = BasePool3Coins(swap).calc_token_amount(_amounts, True)
        elif params[2] == 10:
            _amounts: uint256[4] = [0, 0, 0, 0]
            _amounts[params[0]] = amount
            amount = BasePool4Coins(swap).calc_token_amount(_amounts, True)
        elif params[2] == 11:
            _amounts: uint256[5] = [0, 0, 0, 0, 0]
            _amounts[params[0]] = amount
            amount = BasePool5Coins(swap).calc_token_amount(_amounts, True)
        elif params[2] in [12, 13]:
            # The number of coins doesn't matter here
            amount = BasePool3Coins(swap).calc_withdraw_one_coin(amount, convert(params[1], int128))
        elif params[2] == 14:
            # The number of coins doesn't matter here
            amount = CryptoBasePool3Coins(swap).calc_withdraw_one_coin(amount, params[1])
        elif params[2] in [15, 16]:
            # ETH <--> WETH rate is 1:1
            # ETH ---> stETH rate is 1:1
            # ETH ---> frxETH rate is 1:1
            pass
        elif params[2] == 17:
            if input_token == STETH_ADDRESS:
                amount = wstETH(swap).getWstETHByStETH(amount)
            elif output_token == STETH_ADDRESS:
                amount = wstETH(swap).getStETHByWstETH(amount)
            elif input_token == FRXETH_ADDRESS:
                amount = sfrxETH(swap).convertToShares(amount)
            elif output_token == FRXETH_ADDRESS:
                amount = sfrxETH(swap).convertToAssets(amount)
            else:
                raise "Swap type 17 is for stETH <-> wstETH or frxETH <-> sfrxETH only"
        elif params[2] == 18:
            snx_exchange_rates: address = SynthetixAddressResolver(SNX_ADDRESS_RESOLVER).getAddress(SNX_EXCHANGE_RATES_NAME)
            atomic_amount_and_fee: AtomicAmountAndFee = SynthetixExchanger(snx_exchange_rates).getAmountsForAtomicExchange(
                amount, self.snx_currency_keys[input_token], self.snx_currency_keys[output_token]
            )
            amount = atomic_amount_and_fee.amountReceived
        else:
            raise "Bad swap type"

        # check if this was the last swap
        if i == 4 or _route[i*2+1] == ZERO_ADDRESS:
            break
        # if there is another swap, the output token becomes the input for the next round
        input_token = output_token

    return amount
