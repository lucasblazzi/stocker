import sys
sys.path.append("..")
from utils.api import Api
from utils.db import Database


class News:
    def __init__(self):
        self.api = Api

    @staticmethod
    def _normalize(_news):
        news = {
            "date": str(_news.get("datetime")),
            "title": str(_news.get("headline")),
            "source": str(_news.get("source")),
            "url": str(_news.get("url")),
            "description": str(_news.get("summary")),
            "image": str(_news.get("image")),
        }
        return news

    def news_load(self, symbol):
        _news = {
            "endpoint": "news",
            "symbol": symbol
        }
        news = self.api(_news).get()
        print(news)
        return news

    def insert_news(self, all_news):
        normalized_news = list()
        for _news in all_news:
            news = self._normalize(_news)
            normalized_news.append(news)

        query = """
            INSERT INTO news (date, title, source, url, description, image) VALUES (%(date)s, %(title)s, %(source)s,
             %(url)s, %(description)s, %(image)s);
            """

        try:
            db = Database()
            db.batch_insert(query, normalized_news)
            return True, "Inserção feita com sucesso"

        except Exception as e:
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"