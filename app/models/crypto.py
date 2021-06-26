import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import date
from utils.db_query import insert_crypto_query, crypto_query
from datetime import date


class Crypto:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_crypto):
        crypto = {
            "symbol": str(_crypto.get("symbol")),
            "name": _crypto.get("name"),
            "currency": _crypto.get("currency"),
            "price": round(float(_crypto.get("price")), 10),
            "price_date": date.today(),
        }
        return crypto

    def crypto_load(self):
        _crypto = {
            "endpoint": "crypto_symbols"
        }
        print(f"[API] Crypto")
        crypto = self.api(_crypto).get()
        print(f"[API] {len(crypto)} Cryptos found")
        print(f"[API] SUCCESS")
        for c in crypto:
            _crypto_price = {
                "endpoint": "crypto_prices",
                "symbol": c["symbol"]
            }
            print(f"[API] Crypto Price - {c['symbol']}")
            crypto_price = self.api(_crypto_price).get()
            print(f"[API] SUCCESS")
            c["price"] = crypto_price["price"]
        return crypto

    def insert_crypto(self, _cryptos):
        cryptos = list()
        for c in _cryptos:
            crypto = self._normalize(c)
            cryptos.append(crypto)

        try:
            print(f"[DB] Batch Insert - Crypto")
            db = Database()
            db.batch_insert(insert_crypto_query, cryptos)
            db.close()
            print(f"[DB] SUCCESS")
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"

    @staticmethod
    def select_cryptos(_input):
        arg = f"%{_input}%"
        db = Database()
        result = db.query_arg(crypto_query, (arg,))
        db.close()
        return result