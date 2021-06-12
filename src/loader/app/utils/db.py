import psycopg2

from config import DATABASE
from config import DB_HOST
from config import DB_USER
from config import DB_PASS


class Database:
    def __init__(self, host=DB_HOST, db=DATABASE, user=DB_USER, password=DB_PASS):
        self.conn = psycopg2.connect(host=host, database=db, user=user, password=password)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        results = self.cur.fetchall()
        self.conn.commit()
        return results

    def close(self):
        self.cur.close()
        self.conn.close()


# db = Database()
# result = db.query("SELECT * FROM cliente;"))


# SQL = "INSERT INTO authors (name) VALUES (%s);"
# data = ("O'Reilly", )
# cur.execute(SQL, data)
# testar o comando cur.description