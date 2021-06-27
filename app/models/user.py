import sys
sys.path.append("..")
from utils.db import Database
from utils.db_query import login_query, insert_user_query, update_user_query, select_user_by_id, list_user_query


class User:
    def __init__(self, profile):
        self.profile = profile

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
        print(user)

        return user

    def insert_user(self, _user):
        user = self._normalize(_user)
        db = Database(self.profile)
        c = db.insert_update(insert_user_query, user) or 123
        db.close()
        status = False if c else True
        return status, Database.code_mapper(c, "usuário")

    def update_user(self, _user):
        user = self._normalize(_user)
        db = Database(self.profile)
        c = db.insert_update(update_user_query, user) or 321
        db.close()
        status = False if c else True
        return status, db.code_mapper(c, "usuário")

    def select_user(self, _cpf):
        cpf = int("".join([c for c in _cpf if c.isdigit()]))
        db = Database(self.profile)
        result = db.query_by_id(select_user_by_id, (cpf, ))
        db.close()
        return result

    def get_user_list(self):
        db = Database(self.profile)
        result = db.query(list_user_query)
        db.close()
        return result

    def login(self, _user, _pass):
        db = Database(self.profile)
        result = db.query_by_id(login_query, (_user, _pass))
        db.close()
        return result[0]