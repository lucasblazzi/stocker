import requests
import json
from config import TOKEN as token


def _url(path, version):
    return f"https://sandbox.iexapis.com/{version}/{path}"


def _response_parser(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"Not Found - URL: {response.url}")
    elif response.status_code == 403:
        print(f"Api version error: {response.url}")
    else:
        print(f"An error occurred")


def get_symbols():
    return requests.get(_url("/ref-data/symbols", "stable"), params=token)


def get_crypto_symbols():
    return requests.get(_url("/ref-data/crypto/symbols", "v1"), params=token)


def get_sectors():
    return requests.get(_url("/ref-data/sectors", "v1"), params=token)


def get_sector_performance():
    return requests.get(_url(f"/stock/market/sector-performance", "stable"), params=token)


# doesnt work on sandbox
def get_upcoming_ipo():
    return requests.get(_url(f"/stock/market/upcoming-ipos", "stable"), params=token)


def get_historical(symbol: str, period: str):
    return requests.get(_url(f"/stock/{symbol}/chart/{period}", "v1"), params=token)


def get_company(symbol: str):
    return requests.get(_url(f"/stock/{symbol}/company", "stable"), params=token)


def get_dividends(symbol: str, qtd: int):
    return requests.get(_url(f"/time-series/advanced_dividends/{symbol}?last={qtd}", "stable"), params=token)


def get_return_of_capital(symbol: str, qtd: int):
    return requests.get(_url(f"/time-series/advanced_return_of_capital/{symbol}?last={qtd}", "stable"), params=token)


def get_collection(sector: str):
    return requests.get(_url(f"/stock/market/collection/sector?collectionName={sector}", "stable"), params=token)


def write(m, r):
    with open(f"D:\Documents\GitHub\stocker\mock\{m}_mock.json", "w") as write_file:
        json.dump(r, write_file)
