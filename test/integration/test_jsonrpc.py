import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from lifetioncoind import LifetioncoinDaemon
from lifetioncoin_config import LifetioncoinConfig


def test_lifetioncoind():
    config_text = LifetioncoinConfig.slurp_config_file(config.lifetioncoin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000032e8b86e9e24ba26fbf815aa656bc0aea20227a45c5d1d36f5dbc532ed3'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = LifetioncoinConfig.get_rpc_creds(config_text, network)
    lifetioncoind = LifetioncoinDaemon(**creds)
    assert lifetioncoind.rpc_command is not None

    assert hasattr(lifetioncoind, 'rpc_connection')

    # Lifetioncoin testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = lifetioncoind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert lifetioncoind.rpc_command('getblockhash', 0) == genesis_hash
