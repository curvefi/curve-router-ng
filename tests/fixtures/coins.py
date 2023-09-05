import pytest
from brownie import Contract, project, accounts, ETH_ADDRESS, ZERO_ADDRESS
from brownie.convert import to_bytes
from brownie_tokens import MintableForkToken

interface = project.get_loaded_projects()[0].interface

ETHEREUM_COIN_METHODS = {
    "ATokenMock": {"get_rate": "_get_rate", "mint": "mint"},
    "cERC20": {"get_rate": "exchangeRateStored", "mint": "mint"},
    "IdleToken": {"get_rate": "tokenPrice", "mint": "mintIdleToken"},
    "renERC20": {"get_rate": "exchangeRateCurrent"},
    "yERC20": {"get_rate": "getPricePerFullShare", "mint": "deposit"},
    "aETH": {"get_rate": "ratio"},
    "rETH": {"get_rate": "getExchangeRate"},
    "WETH": {"mint": "deposit"},
}


# public fixtures - these can be used when testing

@pytest.fixture(scope="module")
def coins(coin_dict, network):
    coin_objects = {}
    for coin_name in coin_dict.keys():
        if coin_dict[coin_name]["address"] == ETH_ADDRESS:
            coin_objects[coin_name] = ETH_ADDRESS
            continue
        coin_objects[coin_name] = _get_coin_object(coin_dict[coin_name].get("address"), coin_dict[coin_name].get("interface"), network)

    return coin_objects


@pytest.fixture(scope="module")
def amounts(coin_dict, network):
    _amounts = {}
    for coin_name in coin_dict.keys():
        _amounts[coin_name] = 1000 * 10**coin_dict[coin_name].get("decimals")
        if coin_name in ["sbtc", "sbtc2_lp", "btc.b"]:
            _amounts[coin_name] = 200 * 10 ** coin_dict[coin_name].get("decimals")

    return _amounts


@pytest.fixture(scope="module")
def mint_margo(margo, coins, weth, amounts, network):
    for coin_name in coins.keys():
        amount = amounts[coin_name]
        coin = coins[coin_name]

        balance = margo.balance()
        if coin != ETH_ADDRESS:
            balance = coin.balanceOf(margo)
        if balance >= amount:
            continue

        if coin == ETH_ADDRESS:
            _weth = accounts.at(weth[network], True)
            _weth.transfer(margo, amount)
            continue

        if network == "ethereum":
            if coin.address.lower() == "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb".lower():  # ankrETH
                coin.transfer(margo, amount, {"from": "0x13e252Df0caFe34116cEc052177b7540aFc75F76"})  # steal
                continue
            if coin.address.lower() == "0x9559Aaa82d9649C7A7b220E7c461d2E74c9a3593".lower():  # rETH
                coin.transfer(margo, amount, {"from": "0xa0f75491720835b36edC92D06DDc468D201e9b73"})  # steal from analytico.eth
                continue
            if coin.address.lower() == "0xbBC455cb4F1B9e4bFC4B73970d360c8f032EfEE6".lower():  # sLINK
                coin.transfer(margo, amount, {"from": "0x8D646E10Ee031279400Bc8766b57CC6a53176014"})  # steal from jnewby.eth
                continue

        coin._mint_for_testing(margo, amount, {"from": margo})


@pytest.fixture(scope="module")
def approve_margo(router, margo, coins):
    for coin in coins.values():
        if coin == ETH_ADDRESS or coin.allowance(margo, router) > 2 ** 255:
            continue
        coin.approve(router, 2 ** 256 - 1, {"from": margo})

# private API below


class _MintableTestTokenEthereum(MintableForkToken):
    def __init__(self, address, interface_name):
        super().__init__(address)

        # standardize mint / rate methods
        if interface_name is not None:
            fn_names = ETHEREUM_COIN_METHODS[interface_name]
            for target, attr in fn_names.items():
                if hasattr(self, attr) and target != attr:
                    setattr(self, target, getattr(self, attr))


class _MintableTestTokenOptimism(Contract):
    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1".lower():  # DAI
            self.transfer(target, amount, {"from": "0x7b7b957c284c2c227c980d6e2f804311947b84d0"})
        elif hasattr(self, "l2Bridge"):  # OptimismBridgeToken
            self.mint(target, amount, {"from": self.l2Bridge()})
        elif hasattr(self, "bridge"):  # OptimismBridgeToken2
            self.bridgeMint(target, amount, {"from": self.bridge()})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


class _MintableTestTokenXdai(Contract):
    wrapped = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d".lower()
    eure = "0xcB444e90D8198415266c6a2724b7900fb12FC56E".lower()

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.wrapped:  # WXDAI
            self.transfer(target, amount, {"from": "0xd4e420bBf00b0F409188b338c5D87Df761d6C894"})  # Agave interest bearing WXDAI (agWXDAI)
        elif self.address.lower() == self.eure:  # EURe
            self.transfer(target, amount, {"from": "0xba12222222228d8ba445958a75a0704d566bf2c8"})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


class _MintableTestTokenPolygon(Contract):
    WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi("PolygonToken", address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.WMATIC.lower():  # WMATIC
            self.transfer(target, amount, {"from": "0xadbf1854e5883eb8aa7baf50705338739e558e5b"})
        elif self.address.lower() == "0xb5dfabd7ff7f83bab83995e72a52b97abb7bcf63".lower():  # USDR
            self.transfer(target, amount, {"from": "0xaf0d9d65fc54de245cda37af3d18cbec860a4d4b"})
        elif hasattr(self, "getRoleMember"):  # BridgeToken
            role = "0x8f4f2da22e8ac8f11e15f9fc141cddbb5deea8800186560abb6e68c5496619a9"
            minter = self.getRoleMember(role, 0)
            amount = to_bytes(amount, "bytes32")
            self.deposit(target, amount, {"from": minter})
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestTokenPolygon(self.UNDERLYING_ASSET_ADDRESS(), "BridgeToken")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "set_minter"):  # CurveLpToken
            pool = interface.CurvePool(self.minter())

            amDAI = _MintableTestTokenPolygon(pool.coins(0), "AToken")
            amUSDC = _MintableTestTokenPolygon(pool.coins(1), "AToken")
            amUSDT = _MintableTestTokenPolygon(pool.coins(2), "AToken")

            amounts = [int(amount / 3 * 1.2), int(amount / 10**12 / 3 * 1.2), int(amount / 10**12 / 3 * 1.2)]

            amDAI._mint_for_testing(target, amounts[0])
            amUSDC._mint_for_testing(target, amounts[1])
            amUSDT._mint_for_testing(target, amounts[2])

            amDAI.approve(pool, amounts[0], {"from": target})
            amUSDC.approve(pool, amounts[1], {"from": target})
            amUSDT.approve(pool, amounts[2], {"from": target})

            pool.add_liquidity(amounts, 0, {"from": target})
            if self.balanceOf(target) < amount:
                raise Exception("Not enough aave LP minted")
        elif hasattr(self, "mint"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        else:
            raise ValueError("Unsupported Token")


class _MintableTestTokenFantom(Contract):
    wrapped = "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83"
    underlyingTokens =[
        '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E'.lower(),
        '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75'.lower(),
        '0x049d68029688eAbF473097a2fC38ef61633A3C7A'.lower(),
    ]
    iTokens = [
        '0x04c762a5dF2Fa02FE868F25359E0C259fB811CfE'.lower(),
        '0x328A7b4d538A2b3942653a9983fdA3C12c571141'.lower(),
        '0x70faC71debfD67394D1278D98A29dea79DC6E57A'.lower(),
    ]

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address == self.wrapped:
            # Wrapped Fantom, send from SpookySwap
            self.transfer(target, amount, {"from": "0x2a651563c9d3af67ae0388a5c8f89b867038089e"})
        elif self.address.lower() in self.iTokens:
            idx = self.iTokens.index(self.address.lower())
            underlying_token = _MintableTestTokenFantom(self.underlyingTokens[idx], "AnyswapERC20")
            underlying_amount = int(amount * 10**(underlying_token.decimals() - 8))
            underlying_token._mint_for_testing(target, underlying_amount)
            underlying_token.approve(self.address, underlying_amount, {'from': target})
            self.mint(underlying_amount, {'from': target})
        elif self.address.lower() == "0x27e611fd27b276acbd5ffd632e5eaebec9761e40".lower():  # 2pool LP
            amount = amount // 10**18
            DAI = _MintableTestTokenFantom("0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e", "AnyswapERC20")
            USDC = _MintableTestTokenFantom("0x04068da6c83afcfa0e13ba15a6696662335d5b75", "AnyswapERC20")
            DAI._mint_for_testing(target, (amount // 2) * 10 ** 18)
            USDC._mint_for_testing(target, (amount // 2) * 10 ** 6)

            pool_address = "0x27e611fd27b276acbd5ffd632e5eaebec9761e40"
            DAI.approve(pool_address, 2 ** 256 - 1, {'from': target})
            USDC.approve(pool_address, 2 ** 256 - 1, {'from': target})

            pool = Contract.from_explorer(pool_address)
            pool.add_liquidity([(amount // 2) * 10 ** 18, (amount // 2) * 10 ** 6], 0, {'from': target})
        elif hasattr(self, "Swapin"):  # AnyswapERC20
            tx_hash = to_bytes("0x4475636b204475636b20476f6f7365")
            self.Swapin(tx_hash, target, amount, {"from": self.owner()})
        elif hasattr(self, "POOL"):  # AToken (gToken)
            token = _MintableTestTokenFantom(self.UNDERLYING_ASSET_ADDRESS(), "AnyswapERC20")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


class _MintableTestTokenArbitrum(Contract):
    wrapped = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"

    def __init__(self, address, interface_name):
        if interface_name is not None:
            abi = getattr(interface, interface_name).abi
            self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address == self.wrapped:  # WETH
            self.transfer(target, amount, {"from": "0xba12222222228d8ba445958a75a0704d566bf2c8"})  # Balancer Vault
        elif hasattr(self, "l2Gateway"):  # ArbitrumERC20
            self.bridgeMint(target, amount, {"from": self.l2Gateway()})
        elif hasattr(self, "gatewayAddress"):  # ArbitrumUSDC
            self.bridgeMint(target, amount, {"from": self.gatewayAddress()})
        elif hasattr(self, "bridge"):  # OptimismBridgeToken2
            self.bridgeMint(target, amount, {"from": self.bridge()})
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestTokenArbitrum(self.UNDERLYING_ASSET_ADDRESS(), "ArbitrumERC20")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            try:
                self.mint(target, amount, {"from": self.minter()})
            except Exception:  # 2crv
                USDT = _MintableTestTokenArbitrum("0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", "ArbitrumERC20")
                USDT._mint_for_testing(target, amount // 2)

                USDC = _MintableTestTokenArbitrum("0xff970a61a04b1ca14834a43f5de4533ebddb5cc8", "ArbitrumUSDC")
                USDC._mint_for_testing(target, amount // 2)

                pool_address = "0x7f90122bf0700f9e7e1f688fe926940e8839f353"
                USDT.approve(pool_address, 2 ** 256 - 1, {'from': target})
                USDC.approve(pool_address, 2 ** 256 - 1, {'from': target})

                pool_abi = getattr(interface, "2pool").abi
                pool = Contract.from_abi("2pool", pool_address, pool_abi)
                pool.add_liquidity([amount // 2, amount // 2], 0, {'from': target})  # mint 2CRV
        else:
            raise ValueError("Unsupported Token")


class _MintableTestTokenAvalanche(Contract):
    WAVAX = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"
    USDCT = ["0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E".lower(), "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7".lower()]

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.WAVAX.lower():  # WAVAX
            # Wrapped Avax, send from Iron Bank
            self.transfer(target, amount, {"from": "0xb3c68d69e95b095ab4b33b4cb67dbc0fbf3edf56"})
        elif self.address.lower() in self.USDCT:  # USDC, USDt
            self.transfer(target, amount, {"from": "0x9f8c163cba728e99993abe7495f06c0a3c8ac8b9"})  # Binance: C-Chain Hot Wallet
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestTokenAvalanche(self.UNDERLYING_ASSET_ADDRESS(), "AvalancheERC20")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # Curve LP Token
            try:
                self.mint(target, amount, {"from": self.minter()})
            except Exception:  # 2crv
                USDC = _MintableTestTokenAvalanche("0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e", "AvalancheERC20")
                USDC._mint_for_testing(target, amount // 2 // 10**12)

                USDT = _MintableTestTokenAvalanche("0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7", "AvalancheERC20")
                USDT._mint_for_testing(target, amount // 2 // 10**12)

                pool_address = self.address
                USDT.approve(pool_address, 2 ** 256 - 1, {'from': target})
                USDC.approve(pool_address, 2 ** 256 - 1, {'from': target})

                pool_abi = getattr(interface, "2pool").abi
                pool = Contract.from_abi("2pool", pool_address, pool_abi)
                pool.add_liquidity([amount // 2 // 10**12, amount // 2 // 10**12], 0, {'from': target})  # mint 2CRV
        elif hasattr(self, "mint"):  # AvalancheERC20 (bridge token)
            try:
                self.mint(target, amount, ZERO_ADDRESS, 0, 0x0, {"from": "0xEb1bB70123B2f43419d070d7fDE5618971cc2F8f"})
            except Exception:  # BTC.b
                self.mint(target, amount, ZERO_ADDRESS, 0, 0x0, 0, {"from": "0xF5163f69F97B221d50347Dd79382F11c6401f1a1"})
        else:
            raise ValueError("Unsupported Token")


def _get_coin_object(coin_address, coin_interface, network):
    if network == "ethereum":
        return _MintableTestTokenEthereum(coin_address, coin_interface)
    elif network == "optimism":
        return _MintableTestTokenOptimism(coin_address, coin_interface)
    elif network == "xdai":
        return _MintableTestTokenXdai(coin_address, coin_interface)
    elif network == "polygon":
        return _MintableTestTokenPolygon(coin_address, coin_interface)
    elif network == "fantom":
        return _MintableTestTokenFantom(coin_address, coin_interface)
    elif network == "arbitrum":
        return _MintableTestTokenArbitrum(coin_address, coin_interface)
    elif network == "avalanche":
        return _MintableTestTokenAvalanche(coin_address, coin_interface)
