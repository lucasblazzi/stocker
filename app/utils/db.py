import psycopg2
import psycopg2.extras
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_batch
import psycopg2.errors

from utils.config import DATABASE
from utils.config import DB_HOST
from utils.config import DB_USER
from utils.config import DB_PASS


class Database:
    def __init__(self, host=DB_HOST, db=DATABASE, user=DB_USER, password=DB_PASS):
        self.conn = psycopg2.connect(host=host, database=db, user=user, password=password)
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

    @staticmethod
    def code_mapper(code, obj):
        print(code)
        # https://www.psycopg.org/docs/errors.html
        if code == 606:
            return f"O {obj} já está cadastrado na base de dados."
        elif code == 123:
            return f"{obj.capitalize()} registrado com sucesso"
        elif code == 321:
            return f"{obj.capitalize()} atualizado com sucesso"

    def query(self, query):
        try:
            self.cur.execute(query)
            results = self.cur.fetchall()
            self.conn.commit()
        except psycopg2.OperationalError as e:
            return e.pgcode
        return results

    def query_by_id(self, query, value):
        try:
            self.cur.execute(query, value)
            result = self.cur.fetchone()
            self.conn.commit()
        except psycopg2.OperationalError as e:
            return e.pgcode
        return result

    def query_arg(self, query, value):
        try:
            self.cur.execute(query, value)
            result = self.cur.fetchall()
            self.conn.commit()
        except psycopg2.OperationalError as e:
            return e.pgcode
        return result

    def insert_update(self, query, value):
        try:
            self.cur.execute(query, value)
            self.conn.commit()
        except psycopg2.OperationalError as e:
            return e.pgcode
        except Exception as e:
            print(e)
            return 606

    def batch_insert(self, query, values):
        try:
            execute_batch(self.cur, query, values)
            self.conn.commit()
        except psycopg2.OperationalError as e:
            print(e)
            return e.pgcode
        except Exception as e:
            print(e)
            return 606

    def close(self):
        self.cur.close()
        self.conn.close()
