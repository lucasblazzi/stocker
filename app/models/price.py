import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database


class Price:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_prices):
        prices = list()
        for _price in _prices:
            price = {
                "symbol": _price.get("symbol"),
                "date": _price.get("date"),
                "open": _price.get("open"),
                "close": _price.get("close"),
                "high": _price.get("high"),
                "low": _price.get("low"),
            }
            prices.append(price)
        return prices

    def price_load(self, symbol):
        historical = {
            "endpoint": "historical",
            "symbol": symbol,
            "period": "5y"
        }
        price = self.api(historical).get()
        return price

    def insert_prices(self, _prices):
        prices = self._normalize(_prices)
        query = """
            INSERT INTO price (symbol, date, open, close, high, low) VALUES 
            (%(symbol)s, %(date)s, %(open)s, %(close)s, %(high)s, %(low)s)
            ON CONFLICT (symbol, date) DO UPDATE SET (open, close, high, low)=(%(open)s, %(close)s, %(high)s, %(low)s);
            """
        try:
            db = Database()
            db.batch_insert(query, prices)
            db.close()
            return True, "Inserção feita com sucesso"

        except Exception as e:
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"