import sys
sys.path.append("..")
from utils.db import Database


class Acquisition:

    @staticmethod
    def _normalize(_acquisition):
        acquisition = {
            "symbol": "",
            "client": "",
            "quotas": "",
            "price": "",
            "date": "",
        }
        return acquisition

    def insert_acquisition(self, _acquisition):
        acquisition = self._normalize(_acquisition)
        query = """INSERT INTO acquisition VALUES (%(symbol)s, %(client)s, %(quotas)s, %(price)s, %(date)s);"""

        try:
            db = Database()
            db.insert(query, acquisition)
            db.close()
            return True, "Inserção feita com sucesso"

        except Exception as e:
            return False, f"Ocorreu um erro na inserção no banco de dados: {e}"
