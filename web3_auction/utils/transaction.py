from django.conf import settings
from django.db import transaction
from web3 import Web3
from hexbytes import HexBytes
import environ


env = environ.Env()
if settings.READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(settings.BASE_DIR / ".env"))


WALLET_ADDRESS = env("WALLET_ADDRESS")
PRIVATE_KEY = env("PRIVATE_KEY")
PROVIDER = env("PROVIDER")


def connect_provider():
    try:
        w3 = Web3(Web3.HTTPProvider(PROVIDER))
        if w3.is_connected():
            return w3
    except Exception as e:
        print(f"Falied to connect to {PROVIDER} - {e}")
        return None


def sendTransaction(message):
    try:
        w3 = connect_provider()
        address = WALLET_ADDRESS
        privateKey = PRIVATE_KEY
        gasPrice = w3.eth.gas_price
        nonce = w3.eth.get_transaction_count(address)
        value = w3.to_wei(0, "ether")
        signedTx = w3.eth.account.sign_transaction(
            dict(
                nonce=nonce,
                gasPrice = gasPrice,
                gas=100000,
                to=HexBytes("0x0000000000000000000000000000000000000000"),
                value=value,
                data=message,
            ),
            privateKey,
        )
        print(gasPrice)
        print(message)
        tx = w3.eth.send_raw_transaction(signedTx.rawTransaction)
        txId = w3.to_hex(tx)
        return txId
    except Exception as e:
        print("Falied to send transaction - {e}")
        return None
