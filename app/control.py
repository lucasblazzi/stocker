import streamlit as st
from view import View
from models.data_load import Loader
from models.user import User
from models.company import Company
from models.price import Price
from models.news import News
from models.crypto import Crypto
from utils.db import Database
from psycopg2 import sql
import pandas as pd


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

        elif admin_option == "Ad-Hoc":
            symbols = Company(_profile).get_symbol_list()
            ad_hoc_options = self.view.ad_hoc_form(symbols)
            if ad_hoc_options:
                ad_hoc = self.ad_hoc_compose(ad_hoc_options, _profile)
                self.view.ad_hoc_plot(ad_hoc)

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

    @staticmethod
    def data_shape(results, fields):
        parsed = list()
        for result in results:
            parsed.append({fields[idx]: result[idx] for idx, r in enumerate(result)})
        return parsed

    @staticmethod
    def simple_company_query(filters):
        order = "ASC" if filters["company"]["specific"]["order_method"][0] == "Ascending" else "DESC"

        query = sql.SQL("SELECT {fields} FROM {table} WHERE symbol = ANY(%s) "
                        "ORDER BY {order_by} {order_method} LIMIT {limit}").format(
            fields=sql.SQL(',').join([
                sql.Identifier(field) for field in filters["company"]["specific"]["fields"]]),
            table=sql.Identifier("stocker", "company"),
            order_by=sql.Identifier(filters["company"]["specific"]["order_by"][0]),
            order_method=sql.SQL(order),
            limit=sql.Literal(filters["company"]["specific"]["limit"][0])
        )
        return query

    @staticmethod
    def filter_company_query(filters):
        order = "ASC" if filters["company"]["specific"]["order_method"][0] == "Ascending" else "DESC"
        op = filters["company"]["specific"]["rule_filter"]["operation"]
        if op == "Greater than":
            operation = ">"
        elif op == "Less than":
            operation = "<"
        else:
            operation = "="
        query = sql.SQL("SELECT {fields} FROM {table} WHERE symbol = ANY(%s) AND {field} {operation} {_val}"
                        "ORDER BY {order_by} {order_method} LIMIT {limit}").format(
            fields=sql.SQL(',').join([
                sql.Identifier(field.lower()) for field in filters["company"]["specific"]["fields"]]),
            table=sql.Identifier("stocker", "company"),
            field=sql.Identifier(filters["company"]["specific"]["rule_filter"]["field"]),
            operation=sql.SQL(operation),
            _val=sql.Literal(filters["company"]["specific"]["rule_filter"]["value"]),
            order_by=sql.Identifier(filters["company"]["specific"]["order_by"][0]),
            order_method=sql.SQL(order),
            limit=sql.Literal(filters["company"]["specific"]["limit"][0])
        )
        return query

    @staticmethod
    def filter_news_query(filters):
        order = "ASC" if filters["news"]["order_method"][0] == "Ascending" else "DESC"
        op = filters["news"]["filter_date"]
        if op == "Starting from":
            operation = ">"
        elif op == "Until":
            operation = "<"
        else:
            operation = "="
        query = sql.SQL("SELECT {fields} FROM {table} WHERE symbol = ANY(%s) AND date {operation} {date_input}"
                        " ORDER BY {order_by} {order_method} LIMIT {limit}").format(
            table=sql.Identifier("stocker", "news"),
            fields=sql.SQL(',').join([
                sql.Identifier(field) for field in filters["news"]["fields"]]),
            operation=sql.SQL(operation),
            date_input=sql.Literal(filters["news"]["date"]),
            order_by=sql.Identifier(filters["news"]["order_by"]),
            order_method=sql.SQL(order),
            limit=sql.Literal(filters["news"]["limit"])
        )
        return query

    @staticmethod
    def price_query(filters):
        query = sql.SQL("SELECT date, symbol, {field} FROM {table} WHERE symbol = ANY(%s) "
                        "AND price.date BETWEEN {start_date} AND {end_date}").format(
            table=sql.Identifier("stocker", "price"),
            field=sql.Identifier(filters["price"]["specific"]["type"][0]),
            start_date=sql.Literal(filters["price"]["specific"]["start_date"]),
            end_date=sql.Literal(filters["price"]["specific"]["end_date"]),
        )
        return query

    @staticmethod
    def insight_price_query(compare, _type):
        query = sql.SQL("SELECT symbol, {_type}, date FROM {table} WHERE {_type} = (SELECT {compare}({_type}) FROM {table})").format(
            table=sql.Identifier("stocker", "price"),
            _type=sql.Identifier(_type),
            compare=sql.SQL(compare)
        )
        return query

    def ad_hoc_compose(self, filters, _profile):
        results = {"company": {"specific": [], "insights": {"highest_emp": [], "tech": [], "not_us": []}, "fields": []},
                   "price": {"specific": pd.DataFrame(), "type": None, "insights": {"highest_close": [], "lowest_close": [], "highest_volume": [], "lowest_volume": []}},
                   "news": {"filter": [], "insights": []},
                   "crypto": []}
        if filters["company"]["specific"]["company_list"] and filters["company"]["specific"]["fields"]:
            if not filters["company"]["specific"]["rule_filter"]["apply"]:
                query = self.simple_company_query(filters)
            else:
                query = self.filter_company_query(filters)
            data = Database(_profile).query_arg(query, (filters["company"]["specific"]["company_list"],))
            results["company"]["specific"] = self.data_shape(data, filters["company"]["specific"]["fields"])
            results["company"]["fields"] = filters["company"]["specific"]["fields"]

        if filters["company"]["insights"]["highest_emp"]:
            query = "SELECT c.symbol, c.employees FROM stocker.company c WHERE " \
                    "c.employees = (SELECT MAX(employees) FROM stocker.company)"
            data = Database(_profile).query(query)
            results["company"]["insights"]["highest_emp"] = data

        if filters["company"]["insights"]["tech"]:
            query = "SELECT c.name, c.logo FROM stocker.company c WHERE c.sector = 'Information'"
            data = Database(_profile).query(query)
            results["company"]["insights"]["tech"] = data

        if filters["company"]["insights"]["not_us"]:
            query = "SELECT c.name, c.logo, c.country FROM stocker.company c " \
                    "WHERE c.country != 'US' AND c.country != 'United States'"
            data = Database(_profile).query(query)
            results["company"]["insights"]["not_us"] = data

        if filters["price"]["specific"]["company_list"] and filters["price"]["specific"]["type"]:
            if filters["price"]["specific"]["start_date"] and filters["price"]["specific"]["end_date"]:
                query = self.price_query(filters)
                data = Database(_profile).query_arg(query, (filters["price"]["specific"]["company_list"],))
                if data:
                    prices_df = pd.DataFrame(data, columns=["date", "symbol", filters["price"]["specific"]["type"][0]]).set_index("date")
                else:
                    prices_df = pd.DataFrame()
                results["price"]["specific"] = prices_df
                results["price"]["type"] = filters["price"]["specific"]["type"]
                results["price"]["company_list"] = filters["price"]["specific"]["company_list"]
            else:
                self.view.show_message("st", "warning", "Please fill the date period correctly")

        if filters["price"]["insights"]["highest_close"]:
            query = self.insight_price_query("MAX", "close")
            data = Database(_profile).query(query)
            results["price"]["insights"]["highest_close"] = data

        if filters["price"]["insights"]["lowest_close"]:
            query = self.insight_price_query("MIN", "close")
            data = Database(_profile).query(query)
            results["price"]["insights"]["lowest_close"] = data

        if filters["price"]["insights"]["highest_volume"]:
            query = self.insight_price_query("MAX", "volume")
            data = Database(_profile).query(query)
            results["price"]["insights"]["highest_volume"] = data

        if filters["price"]["insights"]["lowest_volume"]:
            query = self.insight_price_query("MIN", "volume")
            data = Database(_profile).query(query)
            results["price"]["insights"]["lowest_volume"] = data

        if filters["news"]["company_list"]:
            if filters["news"]["fields"] and filters["news"]["filter_date"]:
                query = self.filter_news_query(filters)
                data = Database(_profile).query_arg(query, (filters["news"]["company_list"],))
                results["news"]["filter"] = self.data_shape(data, filters["news"]["fields"])
            else:
                self.view.show_message("st", "warning", "Please fill the fields correctly")

        if filters["news"]["latest"]:
            query = "SELECT * FROM stocker.news n WHERE " \
                    "n.date = (SELECT MAX(date) FROM stocker.news) ORDER BY date DESC LIMIT 1"
            data = Database(_profile).query(query)
            results["news"]["insights"] = data

        if filters["crypto"]["name"]:
            cryptos = Crypto(_profile).select_cryptos(filters["crypto"]["name"])
            results["crypto"] = cryptos[:filters["crypto"]["limit"]]
        Database(_profile).close()
        return results


Control().main()