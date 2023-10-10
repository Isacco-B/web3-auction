from django.conf import settings
from web3 import Web3
from hexbytes import HexBytes
import environ


env = environ.Env()
if settings.READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(settings.BASE_DIR / ".env"))



ADDRESS = env('ADDRESS')
KEY = env('KEY')

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/6f15e1763100444f9579819000fbbd71'))
    address = ADDRESS
    privateKey = KEY
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce = nonce,
        gasPrice = gasPrice,
        gas=100000,
        to = HexBytes('0x0000000000000000000000000000000000000000'),
        value = value,
        data = message.encode('utf-8')
    ), privateKey)


    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId


def get_transaction(hash):
    w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/6f15e1763100444f9579819000fbbd71'))
    transaction = w3.eth.get_transaction(hash)
    transaction_dict = dict(transaction)
    for key, val in transaction_dict.items():
        if 'HexBytes' in str(type(val)):
            transaction_dict[key] = val.hex()
    return transaction_dict


