import requests
from config import TOKEN as token
import json


class API:
    def __init__(self, obj):
        self.endpoint = obj.get("endpoint")
        self.symbol = obj.get("symbol")
        self.sector = obj.get("sector")
        self.period = obj.get("period")
        self.limit = obj.get("limit")
        self.is_mock = obj.get("is_mock", False)

    def _endpoint(self):
        endpoints = {
            "symbols": "/ref-data/symbols",
            "crypto_symbols": "/ref-data/crypto/symbols",
            "sectors": "/ref-data/sectors",
            "sectors_performance": "/stock/market/sector-performance",
            "upcoming_ipos": "/stock/market/upcoming-ipos",
            "company": f"/stock/{self.symbol}/company",
            "historical": f"/stock/{self.symbol}/chart/{self.period}",
            "dividends": f"/time-series/advanced_dividends/{self.symbol}?last={self.limit}",
            "return_of_capital": f"/time-series/advanced_return_of_capital/{self.symbol}?last={self.limit}",
            "collection": f"/stock/market/collection/sector?collectionName={self.sector}",
            "news": f"/time-series/news/{self.symbol}?range={self.period}&limit={self.limit}"
        }
        return endpoints.get(self.endpoint)

    @staticmethod
    def _url(path):
        return f"https://sandbox.iexapis.com/stable{path}"

    @staticmethod
    def _response_parser(response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Not Found - URL: {response.url}")
        elif response.status_code == 403:
            print(f"Api version error: {response.url}")
        else:
            print(f"An error occurred")

    def mock(self):
        r = self.get()
        with open(f"D:\Documents\GitHub\stocker\mock\{self.endpoint}_mock.json", "w") as write_file:
            json.dump(r, write_file)

    def get(self):
        path = self._endpoint()
        r = requests.get(self._url(path=path), params=token)
        return self._response_parser(r)
