import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from grandmastercoin_config import GrandMasterCoinConfig


@pytest.fixture
def grandmastercoin_conf(**kwargs):
    defaults = {
        'rpcuser': 'grandmastercoinrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    grandmastercoin_config = grandmastercoin_conf()
    creds = GrandMasterCoinConfig.get_rpc_creds(grandmastercoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'grandmastercoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    grandmastercoin_config = grandmastercoin_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = GrandMasterCoinConfig.get_rpc_creds(grandmastercoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'grandmastercoinrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', grandmastercoin_conf(), re.M)
    creds = GrandMasterCoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'grandmastercoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 24936


# ensure grandmastercoin network (mainnet, testnet) matches that specified in config
# requires running grandmastercoind on whatever port specified...
#
# This is more of a grandmastercoind/jsonrpc test than a config test...
