import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import datetime

class Price:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_prices):
        prices = list()
        for _price in _prices:
            price = {
                "symbol": str(_price.get("symbol")),
                "date": datetime.strptime(_price.get("date"), "%Y-%m-%d"),
                "open": round(float(_price.get("open")), 4),
                "close": round(float(_price.get("close")), 4),
                "high": round(float(_price.get("high")), 4),
                "low": round(float(_price.get("low")), 4),
                "volume": int(_price.get("volume")),
            }
            prices.append(price)
        return prices

    def price_load(self, symbol, period):
        historical = {
            "endpoint": "historical",
            "symbol": symbol,
            "period": period
        }
        price = self.api(historical).get()
        return price

    def insert_prices(self, _prices):
        prices = self._normalize(_prices)
        query = """
            INSERT INTO stocker.price (symbol, date, open, close, high, low, volume) VALUES 
            (%(symbol)s, %(date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(volume)s)
            ON CONFLICT (symbol, date) DO UPDATE SET (open, close, high, low, volume)=(%(open)s, %(close)s, %(high)s, 
            %(low)s, %(volume)s);
            """
        try:
            db = Database()
            db.batch_insert(query, prices)
            db.close()
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"