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
        option = self.side_bar.selectbox("Options:", ("Research", ))
        if option == "Research":
            self.st.header("Advisor Research Area")
            self.st.markdown("___")
        return option

    def research_area(self):
        execute = False
        args = {"price": {"enabled": False}, "sector": {"enabled": False}, "news": {"enabled": False},
                "company_info": {"enabled": False}, "volatility": {"enabled": False}, "return": {"enabled": False},
                "raw_price": {"enabled": False}, "volume": {"enabled": False}}
        self.st.markdown("___")
        check_cols = self.st.beta_columns(5)

        args["price"]["enabled"] = check_cols[0].checkbox("Price")
        args["company_info"]["enabled"] = check_cols[1].checkbox("Company Information")
        args["sector"]["enabled"] = check_cols[2].checkbox("Sector Distribution")
        args["news"]["enabled"] = check_cols[3].checkbox("News")

        if args["price"]["enabled"]:
            self.st.markdown("___")
            self.st.subheader("Price Insights")
            price_cols = self.st.beta_columns(7)
            args["price"]["_type"] = price_cols[0].selectbox("Price type:", ("close", "open", "high", "low"))
            args["price"]["period"] = price_cols[1].selectbox("Period:", ("ytd", "1m", "6m", "1y", "2y", "5y", "max"))
            args["raw_price"]["enabled"] = price_cols[3].checkbox("Raw Price")
            args["volume"]["enabled"] = price_cols[4].checkbox("Volume")
            args["return"]["enabled"] = price_cols[5].checkbox("Return")
            args["volatility"]["enabled"] = price_cols[6].checkbox("Volatility")
        return execute, args

    def show_cryptos(self, cryptos):
        for crypto in cryptos:
            cols = self.st.beta_columns(3)
            cols[0].markdown(f"**Symbol: ** {crypto.get('symbol', '-')}")
            cols[1].markdown(f"**Name: ** {crypto.get('name', '-')}")
            cols[2].markdown(f"**Price: ** {crypto.get('price', '-')}")

    def crypto_form(self):
        self.st.markdown("<br><br>", unsafe_allow_html=True)
        self.st.markdown("___")
        _input = self.st.text_input("Cryptocurrency")
        return _input

    def sector_distribution(self, sectors):
        self.st.subheader("Sector Distribution")
        r = sectors['sector'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=r.index, values=r)])
        fig.update_layout(
            width=600, height=600,
        )
        self.st.plotly_chart(fig)

    def plot_price(self, prices, _type):
        self.st.subheader(_type.capitalize())
        fig = go.Figure()
        for price in prices:
            name = price["symbol"][0]
            fig.add_trace(go.Scatter(x=price.index, y=price[_type],
                                     mode='lines',
                                     name=name))
        fig.update_layout(
            template="plotly_white",
            width=1400, height=500,
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        self.st.plotly_chart(fig)

    def show_companies(self, companies):
        self.st.markdown("___")
        self.st.subheader("Company Information")
        self.st.markdown("<br>", unsafe_allow_html=True)

        for company in companies:
            basic = self.st.beta_columns(4)
            basic[0].markdown(f"## **{company['name']} ({company['symbol']})**")
            if company.get("logo"):
                basic[3].image(company.get("logo"), width=50)
            basic[3].markdown("<br>", unsafe_allow_html=True)

            desc = self.st.beta_columns(2)
            desc[0].markdown(f"**Sector: ** {company.get('sector', '-')}")
            desc[1].markdown(f"**Industry: ** {company.get('industry', '-')}")
            desc[0].markdown(f"**Description: ** {company.get('description', '-')}")

            info = self.st.beta_columns(2)
            info[0].markdown(f"**CEO: ** {company.get('CEO', '-')}")
            info[1].markdown(f"**Employees: ** {company.get('employees', '-')}")
            info[0].markdown(f"**Website: ** {company.get('website', '-')}")
            info[1].markdown(f"**Location: ** {company.get('city', '')} - {company.get('state', '')} - {company.get('country', '')}")
            self.st.markdown("___")

    def show_news(self, news):
        self.st.markdown("___")
        self.st.subheader("Company News")
        self.st.markdown("<br>", unsafe_allow_html=True)

        for n in news:
            self.st.markdown(f"**{n['symbol']} - {n.get('title', '')} [{n.get('date')}]**")
            self.st.markdown(f"**Source: ** {n.get('source', '-')}")
            if n.get("image"):
                self.st.image(n.get("image"), width=300)
            self.st.markdown(f"**Description: ** {n.get('description', '-')}")
            self.st.markdown(f"**Access on: ** {n.get('url', '-')}")
            self.st.markdown("<br><br>", unsafe_allow_html=True)

    def list_advisors(self, advisors):
        for advisor in advisors:
            cols = self.st.beta_columns(3)
            cols[0].markdown(f"**Name: ** {advisor[0]}")
            cols[1].markdown(f"**CPF: ** {advisor[1]}")
            cols[2].markdown(f"**CVM: ** {advisor[2]}")

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
            self.st.markdown("<br><br>", unsafe_allow_html=True)

            self.st.markdown("___")
            self.st.subheader("Stocker Company Loader")
            self.show_message("st", "info", "Stock Loading: Load on our database information about the companies listed"
                                            "on the Stocks Option selected")
            if self.st.button("Load Stocks"):
                execute = True
                arg["loader"] = "company"
            self.st.markdown("<br><br><br>", unsafe_allow_html=True)

            self.st.markdown("___")
            self.st.subheader("Stocker Price Loader")
            self.show_message("st", "info", "Price Loading: Load on our database information about companies daily"
                                            " prices, you can select a specific period")
            arg["period"] = self.st.selectbox("Prices Period:", ("5y", "2y", "1y", "ytd", "6m", "3m", "1m", "5d"))
            if self.st.button("Load Prices"):
                execute = True
                arg["loader"] = "price"
            self.st.markdown("<br><br><br>", unsafe_allow_html=True)

            self.st.markdown("___")
            self.st.subheader("Stocker News Loader")
            self.show_message("st", "info", "News Loading: Load on our database information about the latest news of"
                                            " companies which can impact the market")
            if self.st.button("Load News"):
                execute = True
                arg["loader"] = "news"
            self.st.markdown("<br><br><br>", unsafe_allow_html=True)

            self.st.markdown("___")
            self.st.subheader("Stocker Crypto Loader")
            self.show_message("st", "info", "Crypto Loading: Load on our database information about all "
                                            "cryptocurrencies available on the market")
            if self.st.button("Load Crypto"):
                execute = True
                arg["loader"] = "crypto"
            self.st.markdown("<br><br><br>", unsafe_allow_html=True)

            self.st.markdown("___")
            self.st.subheader("Stocker Full Loader")
            self.show_message("st", "info", "Full Loading: Load on our database all information listed above: companies"
                                            " prices, news and cryptocurrencies")
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

            "password": cols[2].text_input("Senha", max_chars=15, type='password', help="Senha para login"),

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

