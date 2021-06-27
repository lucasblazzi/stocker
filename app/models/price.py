import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from utils.db_query import insert_prices_query, price_series_query, price_series_query2
import pandas as pd


class Price:
    def __init__(self, profile):
        self.profile = profile
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
            db = Database(self.profile)
            db.batch_insert(insert_prices_query, prices)
            db.close()
            print(f"[DB] SUCCESS")
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"

    @staticmethod
    def get_dates(period):
        end_date = datetime.today()
        if period == "1m":
            start_date = end_date - relativedelta(months=1)
        elif period == "6m":
            start_date = end_date - relativedelta(months=6)
        elif period == "1y":
            start_date = end_date - relativedelta(years=1)
        elif period == "2y":
            start_date = end_date - relativedelta(years=2)
        elif period == "3y":
            start_date = end_date - relativedelta(years=3)
        elif period == "5y":
            start_date = end_date - relativedelta(years=5)
        elif period == "ytd":
            start_date = date(end_date.year, 1, 1)
        else:
            start_date = end_date - relativedelta(years=10)
        return start_date, end_date

    def get_prices(self, symbols, period):
        parsed_symbols = " ".join(symbols)
        prices_dfs = list()
        start_date, end_date = self.get_dates(period)
        try:
            db = Database(self.profile)
            prices = db.query_arg(price_series_query2, (parsed_symbols, start_date, end_date))
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