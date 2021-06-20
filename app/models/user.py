import sys
sys.path.append("..")
from utils.db import Database
import logging


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

        if _user.get("profile") == "Client":
            user["birthday"] = ""
            user["city"] = ""
            user["state"] = ""
            user["country"] = ""
            user["suitability"] = ""

        return user

    def insert_user(self, _user):
        query = None
        user = self._normalize(_user)
        if user.get("profile") == "client":
            query = """
                INSERT INTO client VALUES (%(cpf)s, %(name)s, %(username)s, %(password)s, %(email)s,
                    %(profile)s, %(birthday)s, %(city)s, %(state)s, %(country)s, %(suitability)s);
                """
        elif user.get("profile") == "advisor":
            query = """
                INSERT INTO stocker.user VALUES (%(cpf)s, %(name)s, %(username)s, crypt(%(password)s, gen_salt(\'bf\', 8)),
                 %(email)s, %(profile)s, %(cvm_license)s);
                """
        print(query)
        db = Database()
        c = db.insert_update(query, user) or 123
        db.close()
        status = False if c else True
        return status, Database.code_mapper(c, "usuário")

    def update_user(self, _user):
        query = None
        user = self._normalize(_user)
        if user.get("profile") == "client":
            query = """
            UPDATE client SET name=%(name)s, username=%(username)s, password=%(password)s, 
            email=%(email)s, profile=%(profile)s, birthday=%(birthday)s, city=%(city)s, 
            state=%(state)s, country=%(country)s, suitabilty=%(suitability)s 
            WHERE cpf = %(cpf)s;
            """
        elif user.get("profile") == "advisor":
            query = """
                UPDATE stocker.user SET name=%(name)s, username=%(username)s, password=%(password)s, 
                email=%(email)s, profile=%(profile)s, cvm_license=%(cvm_license)s 
                WHERE cpf = %(cpf)s;
                """

        db = Database()
        c = db.insert_update(query, user) or 321
        db.close()
        status = False if c else True
        return status, db.code_mapper(c, "usuário")

    def select_user(self, _cpf, profile):
        query = None
        cpf = int("".join([c for c in _cpf if c.isdigit()]))
        if profile == "advisor":
            query = """SELECT * FROM stocker.user WHERE stocker.user.cpf = %s;"""
        elif profile == "client":
            query = """SELECT * FROM client WHERE client.cpf = %s;"""

        db = Database()
        result = db.query_by_id(query, (cpf, ))
        db.close()
        return result