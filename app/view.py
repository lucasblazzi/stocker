import plotly.graph_objects as go


class View:
    def __init__(self, st):
        self.st = st
        self.st.set_page_config(layout='wide')
        self.side_bar = st.sidebar

    def show_message(self, location, _type, message):
        if location == "sb":
            component = self.side_bar
        else:
            component = self.st

        if _type == "success":
            component.success(message)
        elif _type == "error":
            component.error(message)
        elif _type == "warning":
            component.warning(message)
        elif _type == "info":
            component.info(message)

    def login(self):
        _user = self.side_bar.text_input("Username:")
        _pass = self.side_bar.text_input("Password", type="password")
        return _user, _pass

    def advisor_setup(self):
        execute = False
        args = None
        option = self.side_bar.selectbox("Options:", ("Research", ))
        if option == "Research":
            self.st.header("Advisor Research Area")
            self.st.markdown("___")
        return option

    def research_area(self):
        execute = False
        args = {"price": {"enabled": False}, "sector": {"enabled": False}, "news": {"enabled": False},
                "comapany_info": {"enabled": False}, "dividends": {"enabled": False}}
        self.st.markdown("___")
        check_cols = self.st.beta_columns(5)

        args["price"]["enabled"] = check_cols[0].checkbox("Price")
        args["news"]["enabled"] = check_cols[1].checkbox("News")
        args["comapany_info"]["enabled"] = check_cols[2].checkbox("Company Information")
        args["sector"]["enabled"] = check_cols[3].checkbox("Sector Distribution")
        args["dividends"]["enabled"] = check_cols[4].checkbox("Dividends")

        if args["price"]["enabled"]:
            self.st.markdown("___")
            self.st.subheader("Price Filter")
            price_cols = self.st.beta_columns(5)
            args["price"]["_type"] = price_cols[0].selectbox("Price type:", ("close", "open", "high", "low"))
            args["price"]["period"] = price_cols[1].selectbox("Period:", ("1m", "6m", "1y", "2y", "5y", "max"))
        if args["news"]["enabled"]:
            self.st.markdown("___")
            self.st.subheader("News Filter")
            news_cols = self.st.beta_columns(5)
            args["price"]["period"] = news_cols[0].selectbox("Period:", ("Last", ))
        return execute, args

    def plot_price(self, symbols, prices, _type):
        fig = go.Figure()
        for symbol in symbols:
            mask = prices["symbol"] == symbol
            symbol_df = prices[mask]
            fig.add_trace(go.Scatter(x=symbol_df.index, y=symbol_df[_type],
                                     mode='lines',
                                     name=symbol))
        fig.update_layout(
            template="plotly_white",
            width=1400, height=500,
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        self.st.plotly_chart(fig)

    def symbol_input(self, symbols):
        selected_symbols = self.st.multiselect("Stocks list:", symbols)
        return selected_symbols

    def admin_setup(self):
        option = self.side_bar.selectbox("Option:", ("Data Loader", "Advisors", "Ad-Hoc"))
        execute = False
        arg = None

        self.st.title("Stocker Administration Area")
        self.st.markdown("___")

        if option == "Data Loader":
            arg = dict()
            self.st.header("Stocker Data Loader")
            arg["symbols"] = self.st.selectbox("Stocks Option:", ("Sample", "S&P 100"))

            self.st.markdown("___")
            self.st.subheader("Stocker Company Loader")
            self.show_message("st", "info", "Stock Loading: Load on our database information about the companies listed"
                                            "on the Stocks Option selected")
            if self.st.button("Load Stocks"):
                execute = True
                arg["loader"] = "company"

            self.st.markdown("___")
            self.st.subheader("Stocker Price Loader")
            self.show_message("st", "info", "Price Loading: Load on our database information about companies daily"
                                            " prices, you can select a specific period")
            arg["period"] = self.st.selectbox("Prices Period:", ("5y", "2y", "1y", "ytd", "6m", "3m", "1m", "5d"))
            if self.st.button("Load Prices"):
                execute = True
                arg["loader"] = "price"

            self.st.markdown("___")
            self.st.subheader("Stocker News Loader")
            self.show_message("st", "info", "News Loading: Load on our database information about the latest news of"
                                            " companies which can impact the market")
            if self.st.button("Load News"):
                execute = True
                arg["loader"] = "news"

            self.st.markdown("___")
            self.st.subheader("Stocker Full Loader")
            self.show_message("st", "info", "Full Loading: Load on our database all information listed above: companies"
                                            "prices and news")
            if self.st.button("Full Load"):
                execute = True
                arg["loader"] = "full"

        elif option == "Ad-Hoc":
            self.st.header("Ad-Hoc")

        elif option == "Advisors":
            sub_option = self.st.selectbox("Opções:", ("List Advisors", "Register Advisor", "Edit Advisor"))
            self.st.markdown("___")
            if sub_option == "List Advisors":
                option = sub_option
                execute = True
            elif sub_option == "Register Advisor":
                arg = self.advisor_form(None)
                option = sub_option
                if arg:
                    execute = True
            elif sub_option == "Edit Advisor":
                arg = self.st.text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12")
                execute = True
                option = sub_option
                self.st.markdown("___")
        return option, execute, arg

    def advisor_form(self, advisor):
        cols = self.st.beta_columns([0.5, 0.25, 0.25])
        button = "Update Advisor" if advisor else "Register Advisor"
        advisor = {
            "name": cols[0].text_input("Nome", max_chars=30, type='default', help="Nome Completo",
                                       value=advisor["name"]) if advisor
            else cols[0].text_input("Nome", max_chars=30, type='default', help="Nome Completo"),

            "username": cols[1].text_input("Usuário", max_chars=15, type='default', help="Usuário para login",
                                           value=advisor["username"]) if advisor
            else cols[1].text_input("Usuário", max_chars=15, type='default', help="Usuário para login"),

            "password": cols[2].text_input("Senha", max_chars=15, type='password', help="Senha para login",
                                           value=advisor["password"]) if advisor
            else cols[2].text_input("Senha", max_chars=15, type='password', help="Senha para login"),

            "cpf": advisor["cpf"] if advisor
            else cols[2].text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12"),

            "cvm_license": cols[1].text_input("Lincença CVM", max_chars=10, type='default',
                                              value=advisor["cvm_license"]) if advisor
            else cols[1].text_input("Lincença CVM", max_chars=10, type='default'),

            "email": cols[0].text_input("Email", max_chars=30, type='default', value=advisor["email"]) if advisor
            else cols[0].text_input("Email", max_chars=30, type='default'),

            "profile": "advisor"
        }
        register = self.st.button(button)
        self.st.markdown("___")
        filled = True
        for b in advisor.values():
            if not b:
                filled = False

        if register:
            if not filled:
                self.show_message("st", "warning", "Preencha todos os campos")
            else:
                return advisor

