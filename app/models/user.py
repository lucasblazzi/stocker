import sys
sys.path.append("..")
from utils.db import Database
from utils.db_query import login_query, insert_user_query, update_user_query, select_user_by_id


class User:

    @staticmethod
    def _normalize(_user):
        user = {
            "cpf": int("".join([c for c in _user.get("cpf") if c.isdigit()])),
            "name": _user.get("name"),
            "username": _user.get("username"),
            "password": _user.get("password"),
            "email": _user.get("email"),
            "profile": _user.get("profile"),
            "cvm_license": int("".join([c for c in _user.get("cvm_license") if c.isdigit()]))
        }

        return user

    def insert_user(self, _user):
        user = self._normalize(_user)
        db = Database()
        c = db.insert_update(insert_user_query, user) or 123
        db.close()
        status = False if c else True
        return status, Database.code_mapper(c, "usuário")

    def update_user(self, _user):
        user = self._normalize(_user)
        db = Database()
        c = db.insert_update(update_user_query, user) or 321
        db.close()
        status = False if c else True
        return status, db.code_mapper(c, "usuário")

    @staticmethod
    def select_user(_cpf):
        cpf = int("".join([c for c in _cpf if c.isdigit()]))
        db = Database()
        result = db.query_by_id(select_user_by_id, (cpf, ))
        db.close()
        return result

    @staticmethod
    def login(_user, _pass):
        db = Database()
        result = db.query_by_id(login_query, (_user, _pass))
        db.close()
        return result[0]