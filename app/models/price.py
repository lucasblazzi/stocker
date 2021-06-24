import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import datetime
from utils.db_query import insert_prices_query, price_series_query
import pandas as pd


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
        print(f"[API] Prices - {symbol}")
        price = self.api(historical).get()
        print(f"[API] SUCCESS")
        return price

    def insert_prices(self, _prices):
        prices = self._normalize(_prices)
        try:
            print(f"[DB] Batch Insert - Prices")
            db = Database()
            db.batch_insert(insert_prices_query, prices)
            db.close()
            print(f"[DB] SUCCESS")
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"

    @staticmethod
    def get_prices(symbols, period):
        parsed_symbols = " ".join(symbols)
        prices_dfs = list()
        try:
            db = Database()
            prices = db.query_arg(price_series_query, (parsed_symbols, period))
            db.close()
            prices_df = pd.DataFrame(prices, columns=["symbol", "date", "close", "high", "low", "open", "volume"])
            for symbol in symbols:
                symbol_mask = prices_df["symbol"] == symbol
                symbol_df = prices_df[symbol_mask]
                symbol_df.set_index("date", inplace=True)
                prices_dfs.append(symbol_df)
            return prices_dfs

        except Exception as e:
            print(e)
            return False