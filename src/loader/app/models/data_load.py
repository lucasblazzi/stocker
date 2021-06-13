import sys
sys.path.append("..")
from utils.api import Api
from models.company import Company
from models.price import Price


class Loader:
    def __init__(self):
        self.api = Api
        self.company = Company()
        self.price = Price()

    def get_symbols(self):
        symbols = {
            "endpoint": "symbols"
        }
        return self.api(symbols).get()

    def run_loader(self, _type="basic"):
        companies = list()
        prices = list()

        if _type == "s&p100":
            with open("sp100.txt", "r") as sp:
                symbol_list = [s.split(" ")[0] for s in sp]
        elif _type == "basic":
            symbol_list = ["AAPL", "ADBE", "AMZN", "BRK.B", "CSCO", "GOOGL"]
        else:
            symbols = self.get_symbols()
            symbol_list = [_obj.get("symbol") for _obj in symbols]

        for symbol in symbol_list:
            company = self.company.company_load(symbol=symbol)
            company_prices = self.price.price_load(symbol=symbol)
            companies.append(company)
            prices.extend(company_prices)

        msg1, status1 = self.company.insert_company(_companies=companies)
        msg2, status2 = self.price.insert_prices(_prices=prices)

        if not msg1:
            msg = msg1
            status = status1
        else:
            msg = msg2
            status = status2

        return msg, status
