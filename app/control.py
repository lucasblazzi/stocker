import streamlit as st
from view import View
from models.data_load import Loader
from models.user import User
from models.company import Company
from models.price import Price
from models.news import News


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
        if admin_option == "Ad-Hoc" and execute:
            st.write("Ad-Hoc")
        elif admin_option == "Data Loader" and execute:
            status = None
            msg = ""

            if arg["loader"] == "full":
                status, msg = Loader().full_loader(_type=arg["symbols"])
            elif arg["loader"] == "company":
                status, msg = Loader().company_loader(_type=arg["symbols"])
            elif arg["loader"] == "price":
                status, msg = Loader().price_loader(_type=arg["symbols"], _period=arg["period"])
            elif arg["loader"] == "news":
                status, msg = Loader().news_loader(_type=arg["symbols"])

            status = "success" if status else "error"
            self.view.show_message("st", status, msg)

        elif admin_option == "Register Advisor" and execute:
            register, status = User().insert_user(arg)
            if register:
                self.view.show_message("st", "success", status)
            else:
                self.view.show_message("st", "error", status)

        elif admin_option == "Edit Advisor" and execute:
            if arg:
                advisor = User().select_user(arg)
                if advisor:
                    updated_advisor = self.view.advisor_form(advisor)
                    if updated_advisor:
                        update, status = User().update_user(updated_advisor)
                        if update:
                            self.view.show_message("st", "success", status)
                        else:
                            self.view.show_message("st", "error", status)

    def advisor_controller(self):
        option = self.view.advisor_setup()
        if option == "Research":
            symbols = Company.get_symbol_list()
            selected_symbols = self.view.symbol_input(sum(symbols, []))
            if selected_symbols:
                execute, arg = self.view.research_area()

                if arg["company_info"]["enabled"]:
                    companies = Company().select_companies(selected_symbols)
                    self.view.show_companies(companies)

                if arg["raw_price"]["enabled"]:
                    prices = Price.get_prices(selected_symbols, arg["price"]["period"])
                    self.view.plot_price(prices, "close")
                    for price in prices:
                        price["volatility"] = price["close"].pct_change(1).fillna(0)
                        price["return"] = price["volatility"].add(1).cumprod().sub(1) * 100

                    if arg["return"]["enabled"]:
                        self.view.plot_price(prices, "return")

                    if arg["volatility"]["enabled"]:
                        self.view.plot_price(prices, "volatility")

                if arg["news"]["enabled"]:
                    news = News().select_news(selected_symbols)
                    self.view.show_news(news)


    def main(self):
        _user, _pass = self.view.login()
        _profile = self.get_profile(_user, _pass)
        if _profile:
            self.view.show_message("sb", "info", f"You are now logged as {_profile}")

            if _profile == "admin":
                self.admin_controller()

            elif _profile == "advisor":
                self.advisor_controller()

        else:
            self.view.show_message("sb", "error", f"Invalid credentials")


Control().main()