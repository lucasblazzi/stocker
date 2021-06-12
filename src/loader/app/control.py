import streamlit as st
from ..main import View


class Control:
    def __init__(self):
        self.st = st
        self.view = View(self.st)

    @staticmethod
    def get_profile(_user, _pass):
        if _user == "advisor" and _pass == "advisor":
            profile = "advisor"
        elif _user == "admin" and _pass == "admin":
            profile = "admin"
        elif _user == "client" and _pass == "client":
            profile = "client"
        else:
            profile = False
        return profile

    def main(self):
        _user, _pass = self.view.login()
        _profile = self.get_profile(_user, _pass)
        if _profile:
            self.view.show_message("sb", "info", f"Você agora está logado como {_profile}")
            if _profile == "admin":
                self.view.admin_setup()
            elif _profile == "advisor":
                self.view.advisor_setup()
            elif _profile == "client":
                self.view.client_setup()
        else:
            self.view.show_message("sb", "error", f"Suas credenciais são inválidas")
