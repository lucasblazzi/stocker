import requests
import json
import sys
sys.path.append("..")
from utils.config import TOKEN
from utils.config import API_URL


class Api:
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
            "company": f"/stock/{self.symbol}/company",
            "historical": f"/stock/{self.symbol}/chart/{self.period}",
            "company_logo": f"/stock/{self.symbol}/logo",
            "news": f"/stock/{self.symbol}/news/last/"
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
