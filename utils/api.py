import requests
import json
from config import TOKEN as token


def _url(path):
    return "https://sandbox.iexapis.com/stable" + path


def get_symbols() -> list:
    return requests.get(_url("/ref-data/symbols"), params=token).json()


def get_crypto_symbols() -> list:
    return requests.get(_url("/ref-data/crypto/symbols"), params=token).json()


def get_sectors() -> list:
    return requests.get(_url("/ref-data/sectors"), params=token).json()


def get_sector_performance() -> list:
    return requests.get(_url(f"/stock/market/sector-performance"), params=token).json()


def get_upcoming_ipo() -> list:
    return requests.get(_url(f"/stock/market/upcoming-ipos"), params=token).json()


def get_historical(symbol: str, period: str, date: str) -> list:
    return requests.get(_url(f"/stock/{symbol}/chart/{period}/{date}"), params=token).json()


def get_company(symbol: str) -> dict:
    return requests.get(_url(f"/stock/{symbol}/company"), params=token).json()


def get_dividends(symbol: str, qtd: int) -> list:
    return requests.get(_url(f"/time-series/advanced_dividends/{symbol}?last={qtd}"), params=token).json()


def get_return_of_capital(symbol: str, qtd: int) -> list:
    return requests.get(_url(f"/time-series/advanced_return_of_capital/{symbol}?last={qtd}"), params=token).json()


def get_collection(sector: str) -> list:
    return requests.get(_url(f"/stock/market/collection/sector?collectionName={sector}"), params=token).json()


try:
    r = get_company(symbol="AAPL")
    print(r)
except json.decoder.JSONDecodeError as e:
    print("Endpoint error")
