import streamlit as st
from main import View
from models.data_load import Loader
from models.user import User

class Control:
    def __init__(self):
        self.st = st
        self.view = View(self.st)

    @staticmethod
    def get_profile(_user, _pass):
        profile = User.login(_user, _pass)
        if _user == "admin" and _pass == "admin":
            profile = "admin"
        return profile

    def admin_controller(self):
        admin_option, execute, arg = self.view.admin_setup()
        if admin_option == "Relatório" and execute:
            st.write("msg")
        elif admin_option == "Carga de dados" and execute:
            status = None
            msg = ""

            if arg["loader"] == "full":
                status, msg = Loader().full_loader(_type=arg["symbols"])
            elif arg["loader"] == "company":
                status, msg = Loader().company_loader(_type=arg["symbols"])
            elif arg["loader"] == "price":
                status, msg = Loader().price_loader(_type=arg["symbols"], _period=arg["period"])
            elif arg["loader"] == "news":
                status, msg = Loader().news_loader(_type="basic")

            status = "success" if status else "error"
            self.view.show_message("st", status, msg)

        elif admin_option == "Registrar Advisor" and execute:
            register, status = User().insert_user(arg)
            if register:
                self.view.show_message("st", "success", status)
            else:
                self.view.show_message("st", "error", status)
        elif admin_option == "Editar Advisor" and execute:
            if arg:
                advisor = User().select_user(arg)
                if advisor:
                    updated_advisor = self.view.advisor_form(advisor)
                    print(updated_advisor)
                    if updated_advisor:
                        update, status = User().update_user(updated_advisor)
                        if update:
                            self.view.show_message("st", "success", status)
                        else:
                            self.view.show_message("st", "error", status)

    def main(self):
        _user, _pass = self.view.login()
        _profile = self.get_profile(_user, _pass)
        if _profile:
            self.view.show_message("sb", "info", f"Você agora está logado como {_profile}")

            if _profile == "admin":
                self.admin_controller()

            elif _profile == "advisor":
                self.view.advisor_setup()

            elif _profile == "client":
                self.view.client_setup()
        else:
            self.view.show_message("sb", "error", f"Suas credenciais são inválidas")


Control().main()