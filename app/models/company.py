import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from utils.db_query import insert_company_query, get_company_list, company_query, sector_query
import pandas as pd


class Company:
    def __init__(self, profile):
        self.profile = profile
        self.api = Api

    @staticmethod
    def _normalize(_company):
        company = {
            "symbol": str(_company.get("symbol")),
            "name": _company.get("companyName"),
            "exchange": _company.get("exchange"),
            "industry": _company.get("industry"),
            "website": _company.get("website"),
            "description": _company.get("description"),
            "CEO": _company.get("CEO"),
            "sector": _company.get("sector"),
            "employees": _company.get("employees"),
            "state": _company.get("state"),
            "city": _company.get("city"),
            "country": _company.get("country"),
            "logo": _company.get("logo"),
        }
        return company

    @staticmethod
    def parse_company_result(result):
        return {
            "symbol": result[0],
            "name": result[1],
            "exchange": result[2],
            "industry": result[3],
            "website": result[4],
            "description": result[5],
            "CEO": result[6],
            "sector": result[7],
            "employees": result[8],
            "state": result[9],
            "city": result[10],
            "country": result[11],
            "logo": result[12]
        }

    def company_load(self, symbol):
        company = {
            "endpoint": "company",
            "symbol": symbol
        }
        logo = {
            "endpoint": "company_logo",
            "symbol": symbol
        }
        print(f"[API] Company - {symbol}")
        company = self.api(company).get()
        print(f"[API] Company Logo - {symbol}")
        logo = self.api(logo).get()
        print(f"[API] SUCCESS")
        company["logo"] = logo.get("url")

        return company

    def insert_company(self, _companies):
        companies = list()
        for _company in _companies:
            company = self._normalize(_company)
            companies.append(company)

        try:
            print(f"[DB] Batch Insert - Company")
            db = Database(self.profile)
            db.batch_insert(insert_company_query, companies)
            db.close()
            print(f"[DB] SUCCESS")
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"

    def get_symbol_list(self):
        try:
            db = Database(self.profile)
            symbols = db.query(get_company_list)
            return symbols
        except Exception as e:
            print(e)
            return []

    def select_companies(self, symbols):
        results = list()
        db = Database(self.profile)
        for symbol in symbols:
            result = db.query_by_id(company_query, (symbol, ))
            parsed = self.parse_company_result(result)
            results.append(parsed)
        db.close()
        return results

    def select_sectors(self, symbols):
        parsed_symbols = " ".join(symbols)
        try:
            db = Database(self.profile)
            sectors = db.query_arg(sector_query, (parsed_symbols, ))
            db.close()

            sectors_df = pd.DataFrame(sectors, columns=["symbol", "sector"])
            return sectors_df
        except Exception as e:
            print(e)
            return False