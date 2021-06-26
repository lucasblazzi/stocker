import json
from models.crypto import Crypto


f = open('crypto.json', )
data = json.load(f)

Crypto().insert_crypto(data)