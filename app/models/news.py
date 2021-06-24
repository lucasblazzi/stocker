import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database
from datetime import datetime
from utils.db_query import insert_news_query, news_query


class News:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_news):
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

    @staticmethod
    def parse_news_result(result):
        return {
            "symbol": result[1],
            "date": result[2],
            "title": result[3],
            "source": result[4],
            "url": result[5],
            "description": result[6],
            "image": result[7]
        }

    def news_load(self, symbol):
        _news = {
            "endpoint": "news",
            "symbol": symbol
        }
        print(f"[API] News - {symbol}")
        news = self.api(_news).get()
        print(f"[API] SUCCESS")
        for n in news:
            n["symbol"] = symbol
        return news

    def insert_news(self, all_news):
        normalized_news = list()
        for _news in all_news:
            news = self._normalize(_news)
            normalized_news.append(news)

        try:
            print(f"[DB] Batch Insert - News")
            db = Database()
            db.batch_insert(insert_news_query, normalized_news)
            db.close()
            print(f"[DB] SUCCESS")
            return True, "Inserção feita com sucesso"

        except Exception as e:
            print(e)
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"

    def select_news(self, symbols):
        results = list()
        db = Database()
        for symbol in symbols:
            result = db.query_by_id(news_query, (symbol, ))
            parsed = self.parse_news_result(result)
            results.append(parsed)
        db.close()
        return results