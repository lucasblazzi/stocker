import streamlit as st
from view import View
from models.data_load import Loader
from models.user import User
from models.company import Company
from models.price import Price
from models.news import News
from models.crypto import Crypto


class Control:
    def __init__(self):
        self.st = st
        self.view = View(self.st)

    @staticmethod
    def get_profile(_user, _pass):
        return User("login").login(_user, _pass)

    def admin_controller(self, _profile):
        admin_option, execute, arg = self.view.admin_setup()
        if admin_option == "Ad-Hoc" and execute:
            st.write("Ad-Hoc")
        elif admin_option == "Data Loader" and execute:
            status = None
            msg = ""

            if arg["loader"] == "full":
                status, msg = Loader(_profile).full_loader(_type=arg["symbols"])
            elif arg["loader"] == "company":
                status, msg = Loader(_profile).company_loader(_type=arg["symbols"])
            elif arg["loader"] == "price":
                status, msg = Loader(_profile).price_loader(_type=arg["symbols"], _period=arg["period"])
            elif arg["loader"] == "news":
                status, msg = Loader(_profile).news_loader(_type=arg["symbols"])
            elif arg["loader"] == "crypto":
                status, msg = Loader(_profile).crypto_loader(_type=arg["symbols"])

            status = "success" if status else "error"
            self.view.show_message("st", status, msg)

        elif admin_option == "Register Advisor" and execute:
            register, status = User(_profile).insert_user(arg)
            if register:
                self.view.show_message("st", "success", status)
            else:
                self.view.show_message("st", "error", status)

        elif admin_option == "Edit Advisor" and execute:
            if arg:
                advisor = User(_profile).select_user(arg)
                if advisor:
                    updated_advisor = self.view.advisor_form(advisor)
                    if updated_advisor:
                        update, status = User(_profile).update_user(updated_advisor)
                        if update:
                            self.view.show_message("st", "success", status)
                        else:
                            self.view.show_message("st", "error", status)
        elif admin_option == "List Advisors":
            advisors = User(_profile).get_user_list()
            self.view.list_advisors(advisors)

    def advisor_controller(self, _profile):
        option = self.view.advisor_setup()
        if option == "Research":
            symbols = Company(_profile).get_symbol_list()
            selected_symbols = self.view.symbol_input(sum(symbols, []))
            if selected_symbols:
                execute, arg = self.view.research_area()

                if arg["price"]["enabled"]:
                    prices = Price(_profile).get_prices(selected_symbols, arg["price"]["period"])
                    for price in prices:
                        price["volatility"] = price["close"].pct_change(1).fillna(0)
                        price["return"] = price["volatility"].add(1).cumprod().sub(1) * 100
                    if arg["raw_price"]["enabled"]:
                        self.view.plot_price(prices, arg["price"]["_type"])
                    if arg["volume"]["enabled"]:
                        self.view.plot_price(prices, "volume")
                    if arg["return"]["enabled"]:
                        self.view.plot_price(prices, "return")
                    if arg["volatility"]["enabled"]:
                        self.view.plot_price(prices, "volatility")

                if arg["company_info"]["enabled"]:
                    companies = Company(_profile).select_companies(selected_symbols)
                    self.view.show_companies(companies)

                if arg["sector"]["enabled"]:
                    sectors = Company(_profile).select_sectors(selected_symbols)
                    self.view.sector_distribution(sectors)

                if arg["news"]["enabled"]:
                    news = News(_profile).select_news(selected_symbols)
                    self.view.show_news(news)

            crypto_input = self.view.crypto_form()
            if crypto_input:
                cryptos = Crypto(_profile).select_cryptos(crypto_input)
                self.view.show_cryptos(cryptos)

    def main(self):
        _user, _pass = self.view.login()
        _profile = self.get_profile(_user, _pass)
        if _profile:
            self.view.show_message("sb", "info", f"You are now logged as {_profile}")

            if _profile == "admin":
                self.admin_controller(_profile)

            elif _profile == "advisor":
                self.advisor_controller(_profile)

        else:
            self.view.show_message("sb", "error", f"Invalid credentials")


Control().main()