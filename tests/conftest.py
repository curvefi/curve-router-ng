#!/usr/bin/python3
import json
import pytest
from pathlib import Path
from brownie import chain
from brownie.project.main import get_loaded_projects


pytest_plugins = [
    "fixtures.accounts",
    "fixtures.coins",
    "fixtures.deployments",
]

_NETWORKS = {
    1: "ethereum",
    10: "optimism",
    100: "xdai",
    137: "polygon",
    250: "fantom",
    42161: "arbitrum",
    43114: "avalanche",
}

_COINDATA = {}

_WETH = {
    "ethereum": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "optimism": "0x4200000000000000000000000000000000000006",
    "xdai": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
    "polygon": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
    "fantom": "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83",
    "arbitrum": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
    "avalanche": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
}


def pytest_addoption(parser):
    parser.addoption("--pools", help="comma-separated list of pools to target")


def pytest_sessionstart():
    # load `pooldata.json` for each pool
    project = get_loaded_projects()[0]

    for network in ["ethereum", "polygon", "arbitrum", "avalanche"]:
        _COINDATA[network] = {}
        with project._path.joinpath(f"constants/{network}.json").open() as fp:
            _COINDATA[network] = json.load(fp)


def pytest_ignore_collect(path, config):
    project = get_loaded_projects()[0]
    path = Path(path).relative_to(project._path)
    test_file = path.parts[1]

    network = config.getoption("network")[0].split("-")[0]
    if network == "mainnet":
        network = "ethereum"
    if not test_file.startswith(f"test_{network}"):
        return True


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


@pytest.fixture(scope="module")
def network():
    return _NETWORKS[chain.id]


@pytest.fixture(scope="module")
def coin_dict(network):
    return _COINDATA[network]


@pytest.fixture(scope="module")
def weth():
    return _WETH
