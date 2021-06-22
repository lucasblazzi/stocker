import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import datetime
from utils.db_query import insert_news_query


class News:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_news):
        print(_news)
        news = {
            "symbol": str(_news.get("symbol")),
            "date": datetime.fromtimestamp(_news.get("datetime")/1000.0),
            "title": str(_news.get("headline")),
            "source": str(_news.get("source")),
            "url": _news.get("url"),
            "description": str(_news.get("summary")),
            "image": _news.get("image"),
        }
        return news

    def news_load(self, symbol):
        _news = {
            "endpoint": "news",
            "symbol": symbol
        }
        news = self.api(_news).get()
        for n in news:
            n["symbol"] = symbol
        return news

    def insert_news(self, all_news):
        normalized_news = list()
        for _news in all_news:
            news = self._normalize(_news)
            normalized_news.append(news)

        try:
            db = Database()
            db.batch_insert(insert_news_query, normalized_news)
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"