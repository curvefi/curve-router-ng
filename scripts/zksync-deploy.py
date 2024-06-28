import os
import json
import boa
from getpass import getpass
import boa_zksync
from eth_account import account

zksync_rpc = "https://mainnet.era.zksync.io"

boa_zksync.set_zksync_env(zksync_rpc)


def account_load(fname):
    path = os.path.expanduser(os.path.join('~', '.brownie', 'accounts', fname + '.json'))
    with open(path, 'r') as f:
        pkey = account.decode_keyfile_json(json.load(f), getpass())
        return account.Account.from_key(pkey)


def main():
    boa.env.add_account(account_load('curve-deployer'))
    boa.load("contracts/RouterNgPoolsOnly.vy", "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91")


if __name__ == "__main__":
    main()
