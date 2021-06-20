import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database


class Company:
    def __init__(self):
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

    def company_load(self, symbol):
        company = {
            "endpoint": "company",
            "symbol": symbol
        }
        logo = {
            "endpoint": "company_logo",
            "symbol": symbol
        }

        company = self.api(company).get()
        logo = self.api(logo).get()
        company["logo"] = logo.get("url")

        return company

    def insert_company(self, _companies):
        companies = list()
        for _company in _companies:
            company = self._normalize(_company)
            companies.append(company)

        query = """
            INSERT INTO stocker.company (symbol, name, exchange, industry, website, description, CEO, sector, 
                employees, state, city, country, logo) VALUES (%(symbol)s, %(name)s, %(exchange)s, %(industry)s,
                %(website)s, %(description)s, %(CEO)s, %(sector)s, %(employees)s, %(state)s, %(city)s, %(country)s,
                %(logo)s)
            ON CONFLICT (symbol) DO UPDATE SET (name, exchange, industry, website, description, CEO, sector, 
                employees, state, city, country, logo)=(%(name)s, %(exchange)s, %(industry)s, %(website)s,
                %(description)s, %(CEO)s, %(sector)s, %(employees)s, %(state)s, %(city)s, %(country)s, %(logo)s);
            """

        try:
            db = Database()
            db.batch_insert(query, companies)
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"