"""Verifies that all providers of blockchain data are consistent with others."""
import unittest
try:
    from boltzmann.utils.bitcoind_rpc_wrapper import BitcoindRPCWrapper
    from boltzmann.utils.bci_wrapper import BlockchainInfoWrapper
except ImportError:
    import sys
    import os
    # Adds boltzmann directory into path
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
    from boltzmann.utils.bitcoind_rpc_wrapper import BitcoindRPCWrapper
    from boltzmann.utils.bci_wrapper import BlockchainInfoWrapper


class CompareTest(unittest.TestCase):
    """Compare the results of various providers for given transaction IDs."""

    PROVIDERS = [BitcoindRPCWrapper, BlockchainInfoWrapper]

    #a list of transactions with expected data
    TEST_TXS = [
        {'height': 100001,
         'time': 1293624404,
         'txid': '8131ffb0a2c945ecaf9b9063e59558784f9c3a74741ce6ae2a18d0571dac15bb',
         'inputs': [{'n': 0,
                     'value': 5000000000,
                     'address': '1HYAekgNKqQiCadt3fnKdLQFFNLFHPPnCR',
                     'tx_idx': 239354
                    },
                    {'n': 0,
                     'value': 5000000000,
                     'address': '16hwoJvz1xje8HBgoLZcxwo1CwE3cvkb17',
                     'tx_idx': 239356
                    },
                    {'n': 0,
                     'value': 5000000000,
                     'address': '1KWGBfAsuBFzKQ7bhSJV5WbgVNvvQ5R1j2',
                     'tx_idx': 239322
                    },
                    {'n': 0,
                     'value': 5000000000,
                     'address': '15XgnazTwLj7sNPkbUo5vCSKBmR43X5vW4',
                     'tx_idx': 239205
                    },
                    {'n': 0,
                     'value': 5001000000,
                     'address': '16HjHvF5umsgAzaX2ddosB81ttkrVHkvqo',
                     'tx_idx': 239162
                    }],
         'outputs': [{'n': 0,
                      'value': 25000000000,
                      'address': '15xif4SjXiFi3NDEsmMZCfTdE9jvvVQrjU',
                      'tx_idx': 240051
                     },
                     {'n': 1,
                      'value': 1000000,
                      'address': '1NkKLMgbSjXrT7oHagnGmYFhXAWXjJsKCj',
                      'tx_idx': 240051
                     }]
        },
        {'height': 299173,
         'time': 1399267359,
         'txid': '8e56317360a548e8ef28ec475878ef70d1371bee3526c017ac22ad61ae5740b8',
         'inputs': [{'n': 0,
                     'value': 10000000,
                     'address': '1FJNUgMPRyBx6ahPmsH6jiYZHDWBPEHfU7',
                     'tx_idx': 55795695
                    },
                    {'n': 1,
                     'value': 1380000,
                     'address': '1JDHTo412L9RCtuGbYw4MBeL1xn7ZTuzLH',
                     'tx_idx': 55462552
                    }],
         'outputs': [{'n': 0,
                      'value': 100000,
                      'address': '1JR3x2xNfeFicqJcvzz1gkEhHEewJBb5Zb',
                      'tx_idx': 55819527
                     },
                     {'n': 1,
                      'value': 9850000,
                      'address': '18JNSFk8eRZcM8RdqLDSgCiipgnfAYsFef',
                      'tx_idx': 55819527
                     },
                     {'n': 2,
                      'value': 100000,
                      'address': '1ALKUqxRb2MeFqomLCqeYwDZK6FvLNnP3H',
                      'tx_idx': 55819527
                     },
                     {'n': 3,
                      'value': 1270000,
                      'address': '1PA1eHufj8axDWEbYfPtL8HXfA66gTFsFc',
                      'tx_idx': 55819527
                     }
                    ]
        }]
    '''
        TODO:Both of these currently raise exception for BCI, so shouldnt work for RPC either
        { #genesis block coinbase tx
            'height': 0,
            'time': 1231006505,
            'txid': '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
            'inputs': [{}], #TODO
            'outputs': [{}] #TODO
        },
        { #BIP30 duplicate tx, see:
          #https://github.com/kristovatlas/interesting-bitcoin-data
            'height': 91842, #also height 91812
            'time': 1289757588,
            'txid': 'd5d27987d2a3dfc724e359870c6644b40e497bdc0589a033220fe15429d88599',
            'inputs': [{}], #TODO
            'outputs': [{}] #TODO
        }
    '''

    def test(self):
        """Verify that fields are present and as expected for each data provider."""
        for test_idx, expected_tx in enumerate(self.TEST_TXS):
            for provider in self.PROVIDERS:
                prov = provider()
                print("Starting test # {0}".format(test_idx+1))
                txn = prov.get_tx(expected_tx['txid'])
                _assertEq(expected_tx['txid'], txn.txid, test_idx+1)
                _assertNoneOrEqual(txn.time, expected_tx['time'], test_idx+1)
                _assertEq(
                    len(expected_tx['inputs']), len(txn.inputs), test_idx+1)
                _assertEq(
                    len(expected_tx['outputs']), len(txn.outputs), test_idx+1)
                for idx, tx_in in enumerate(expected_tx['inputs']):
                    _assertEq(tx_in['n'], txn.inputs[idx].n, test_idx+1)
                    _assertEq(tx_in['value'], txn.inputs[idx].value, test_idx+1)
                    _assertEq(
                        tx_in['address'], txn.inputs[idx].address, test_idx+1)
                    _assertNoneOrEqual(
                        txn.inputs[idx].tx_idx, tx_in['tx_idx'], test_idx+1)
                for idx, tx_out in enumerate(expected_tx['outputs']):
                    _assertEq(tx_out['n'], txn.outputs[idx].n, test_idx+1)
                    _assertEq(
                        tx_out['value'], txn.outputs[idx].value, test_idx+1)
                    _assertEq(
                        tx_out['address'], txn.outputs[idx].address, test_idx+1)
                    _assertNoneOrEqual(
                        txn.outputs[idx].tx_idx, tx_out['tx_idx'], test_idx+1)

def _assertEq(a, b, test_num):
    assert a == b, "Test {0}: {1} != {2}".format(test_num, a, b)

def _assertNoneOrEqual(a, b, test_num):
    assert a is None or a == b, \
        "Test {0}: {1} != None && != {2}".format(test_num, a, b)

if __name__ == '__main__':
    unittest.main()
