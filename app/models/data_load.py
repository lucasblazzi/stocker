import sys
sys.path.append("..")
import json

from utils.api import Api
from models.company import Company
from models.price import Price
from models.news import News
from models.crypto import Crypto


class Loader:
    def __init__(self):
        self.api = Api
        self.company = Company()
        self.price = Price()
        self.news = News()
        self.crypto = Crypto()

    @staticmethod
    def backup(name, items):
        with open(f"{name}.json", "w") as file:
            json.dump(items, file)

    def get_symbols(self, _type):
        if _type == "S&P 100":
            with open("sp100.txt", "r") as sp:
                symbol_list = [s.split(" ")[0] for s in sp]
        elif _type == "full":
            symbols = self.api({"endpoint": "symbols"}).get()
            symbol_list = [_obj.get("symbol") for _obj in symbols]
        else:
            symbol_list = ["AAPL", "ADBE", "AMZN", "BRK.B", "CSCO", "GOOGL"]
        return symbol_list

    def news_loader(self, _type="Sample"):
        news = list()
        symbol_list = self.get_symbols(_type)
        for symbol in symbol_list:
            company_news = self.news.news_load(symbol=symbol)
            news.extend(company_news)

        self.backup("news", news)
        msg, status = self.news.insert_news(all_news=news)
        return msg, status

    def price_loader(self, _type="Sample", _period="5y"):
        prices = list()
        symbol_list = self.get_symbols(_type)
        for symbol in symbol_list:
            company_prices = self.price.price_load(symbol=symbol, period=_period)
            prices.extend(company_prices)

        self.backup("price", prices)
        msg, status = self.price.insert_prices(_prices=prices)
        return msg, status

    def company_loader(self, _type="Sample"):
        companies = list()
        symbol_list = self.get_symbols(_type)
        for symbol in symbol_list:
            company = self.company.company_load(symbol=symbol)
            companies.append(company)

        self.backup("company", companies)
        msg, status = self.company.insert_company(_companies=companies)
        return msg, status

    def crypto_loader(self, _type="Sample"):
        cryptos = self.crypto.crypto_load()
        self.backup("crypto", cryptos)
        msg, status = self.crypto.insert_crypto(_cryptos=cryptos)
        return msg, status

    def full_loader(self, _type="Sample"):
        companies = list()
        prices = list()
        news = list()
        cryptos = list()

        symbol_list = self.get_symbols(_type)

        for symbol in symbol_list:
            company = self.company.company_load(symbol=symbol)
            company_prices = self.price.price_load(symbol=symbol, period="5y")
            company_news = self.news.news_load(symbol=symbol)
            cryptos = self.crypto.crypto_load()
            companies.append(company)
            prices.extend(company_prices)
            news.extend(company_news)

        msg1, status1 = self.company.insert_company(_companies=companies)
        msg2, status2 = self.price.insert_prices(_prices=prices)
        msg3, status3 = self.news.insert_news(all_news=news)
        msg4, status4 = self.crypto.insert_crypto(_cryptos=cryptos)

        if msg1:
            msg = msg1
            status = status1
        elif msg2:
            msg = msg2
            status = status2
        elif msg3:
            msg = msg3
            status = status3
        else:
            msg = msg4
            status = status4

        return msg, status
