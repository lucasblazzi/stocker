import requests
import json

from config import TOKEN
from config import API_URL


class API:
    def __init__(self, obj):
        self.endpoint = obj.get("endpoint")
        self.symbol = obj.get("symbol")
        self.sector = obj.get("sector")
        self.period = obj.get("period")
        self.limit = obj.get("limit")

    def _endpoint(self):
        endpoints = {
            "symbols": "/ref-data/symbols",
            "sectors": "/ref-data/sectors",
            "sectors_performance": "/stock/market/sector-performance",
            "company": f"/stock/{self.symbol}/company",
            "historical": f"/stock/{self.symbol}/chart/{self.period}",
        }
        return endpoints.get(self.endpoint)

    @staticmethod
    def _url(path):
        return f"{API_URL}{path}"

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
        r = requests.get(self._url(path=path), params=TOKEN)
        return self._response_parser(r)



symbol = "AAPL"

_obj = {
    "endpoint": "collection",
    "symbol": "AAPL",
    "period": "1y",
    "limit": 10,
    "sector": "Technology"
}
API(_obj).mock()
