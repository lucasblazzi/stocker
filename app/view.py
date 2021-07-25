import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
        check_cols = self.st.beta_columns(4)

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
            width=400, height=400,
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
            basic[0].markdown(f"## **{company.get('name', ' ')} ({company.get('symbol', ' ')})**")
            if company.get("logo"):
                basic[3].image(company.get("logo"), width=50)
            basic[3].markdown("<br>", unsafe_allow_html=True)

            desc = self.st.beta_columns(2)
            if company.get('sector'):
                desc[0].markdown(f"**Sector: ** {company.get('sector', '-')}")
            if company.get('industry'):
                desc[1].markdown(f"**Industry: ** {company.get('industry', '-')}")
            if company.get('description'):
                desc[0].markdown(f"**Description: ** {company.get('description', '-')}")

            info = self.st.beta_columns(2)
            if company.get('CEO'):
                info[0].markdown(f"**CEO: ** {company.get('CEO', '-')}")
            if company.get('employees'):
                info[1].markdown(f"**Employees: ** {company.get('employees', '-')}")
            if company.get('website'):
                info[0].markdown(f"**Website: ** {company.get('website', '-')}")
            if company.get('city') or company.get('state') or company.get('country'):
                info[1].markdown(f"**Location: ** {company.get('city', ' ')} - {company.get('state', ' ')} - {company.get('country', ' ')}")
            self.st.markdown("___")

    def show_news(self, news, title="Company News"):
        self.st.markdown("___")
        self.st.subheader(title)
        self.st.markdown("<br>", unsafe_allow_html=True)

        for n in news:
            if n.get('symbol') or n.get('title') or n.get('date'):
                self.st.markdown(f"**{n.get('symbol', ' ')} - {n.get('title', ' ')} [{n.get('date', ' ')}]**")
            if n.get('source'):
                self.st.markdown(f"**Source: ** {n.get('source', '-')}")
            if n.get("image"):
                self.st.image(n.get("image"), width=300)
            if n.get("description"):
                self.st.markdown(f"**Description: ** {n.get('description', '-')}")
            if n.get("url"):
                self.st.markdown(f"**Access on: ** {n.get('url', '-')}")
            self.st.markdown("<br>", unsafe_allow_html=True)

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

    @staticmethod
    def plot_bar(companies, x, y, title, color):
        df = pd.DataFrame(companies)
        fig = px.bar(df, x=x, y=y,
                     color=color, title=title,
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     height=400)
        return fig

    @staticmethod
    def plot_bar2(companies, y, title):
        df = pd.DataFrame(companies)[["symbol", y]]
        r = df[y].value_counts()
        fig = go.Figure(data=[go.Bar(x=df[y], y=r)])
        fig.update_layout(
            height=400,
            title=title
        )
        return fig

    @staticmethod
    def plot_pie(companies, y, title):
        df = pd.DataFrame(companies)[["symbol", y]]
        r = df[y].value_counts()
        fig = go.Figure(data=[go.Pie(labels=df[y], values=r)])
        fig.update_layout(
            height=400,
            title=title
        )
        return fig

    @staticmethod
    def plot_highest_emp(highest_emp):
        fig = go.Figure(data=[go.Indicator(
            mode="number+delta",
            value=highest_emp[0][1],
            title={
                "text": f"{highest_emp[0][0]}<br><span style='font-size:0.8em;color:gray'>Highest number</span><br>"
                        f"<span style='font-size:0.8em;color:gray'>of employees</span>"},
            )])
        return fig

    @staticmethod
    def plot_information_companies(cols, companies):
        logos = [company[1] for company in companies]
        names = [company[0] for company in companies]
        for idx, logo in enumerate(logos):
            col = 2 if idx % 2 == 0 else 3
            cols[col].image(logo, width=50)
        for idx, name in enumerate(names):
            col = 0 if idx % 2 == 0 else 1
            cols[col].markdown(f"**Name: ** {name}")

    @staticmethod
    def plot_notusa_companies(cols, companies):
        for company in companies:
            cols[0].markdown(f"**Name: ** {company[0]}")
            cols[1].markdown(f"**Country: ** {company[2]}")
            cols[2].image(company[1], width=50)

    @staticmethod
    def plot_insight_prices(k, v):
        fig = go.Figure(data=[go.Indicator(
            mode="number+delta",
            value=v[0][1],
            title={
                "text": f"{v[0][0]}<br><span style='font-size:0.8em;color:gray'>{k.split('_')[0].capitalize()} {k.split('_')[1].capitalize()}</span><br>"
                        f"<span style='font-size:0.8em;color:gray'>{v[0][2]}</span>"},
            )])
        return fig

    def plot_company_ad_hoc(self, results):
        companies = results["company"]["specific"]
        highest_emp = results["company"]["insights"]["highest_emp"]
        information = results["company"]["insights"]["tech"]
        not_usa = results["company"]["insights"]["not_us"]
        fields = results["company"]["fields"]
        if companies:
            if not "symbol" in fields:
                self.st.warning("Be sure to select the symbol option")
            else:
                self.show_companies(companies)
                col = self.st.beta_columns(2)
                if "employees" in fields:
                    fig1 = self.plot_bar(companies, "symbol", "employees", "Number of employees by company", "employees")
                    col[0].plotly_chart(fig1, use_container_width=True)
                if "state" in fields:
                    fig2 = self.plot_bar2(companies, "state", "State distribution")
                    col[1].plotly_chart(fig2, use_container_width=True)
                col2 = self.st.beta_columns(2)
                if "sector" in fields:
                    fig3 = self.plot_pie(companies, "sector", "Companies by sector")
                    col2[0].plotly_chart(fig3, use_container_width=True)
                if "industry" in fields:
                    fig4 = self.plot_pie(companies, "industry", "Companies by industry")
                    col2[1].plotly_chart(fig4, use_container_width=True)

        if highest_emp:
            fig5 = self.plot_highest_emp(highest_emp)
            self.st.plotly_chart(fig5, use_container_width=True)
        if information:
            self.st.markdown("___")
            title_col = self.st.beta_columns(1)
            cols4 = self.st.beta_columns([1, 1, 0.2, 0.2])
            title_col[0].subheader("Information sector companies")
            self.plot_information_companies(cols4, information)
        if not_usa:
            self.st.markdown("___")
            title_col2 = self.st.beta_columns(1)
            title_col2[0].subheader("Nasdaq listed companies outside USA")
            cols5 = self.st.beta_columns(4)
            self.plot_notusa_companies(cols5, not_usa)

    def plot_price_ad_hoc(self, results):
        if not results["price"]["specific"].empty:
            self.st.markdown("___")
            dfs = list()
            for company in results["price"]["company_list"]:
                mask = (results["price"]["specific"]["symbol"] == company)
                dfs.append(results["price"]["specific"][mask])
            self.plot_price(dfs, results["price"]["type"][0])

        self.st.markdown("___")
        c = 0
        cols = self.st.beta_columns(len(results["price"]["insights"].keys()))
        for k, val in results["price"]["insights"].items():
            if val:
                cols[c].plotly_chart(self.plot_insight_prices(k, val), use_container_width=True)
                c += 1

    def plot_news_ad_hoc(self, results):
        if results["news"]["filter"]:
            self.show_news(results["news"]["filter"], "Filtered News")
        if results["news"]["insights"]:
            news_fields = ("id", "symbol", "date", "title", "source", "url", "description", "image")
            latest = results["news"]["insights"][0]
            latest_news = dict()
            for idx, v in enumerate(latest):
                latest_news[news_fields[idx]] = v
            self.show_news([latest], f"Latest news - {latest['symbol']} - {latest['date']}")

    def plot_crypto_ad_hoc(self, results):
        if results["crypto"]:
            self.st.markdown("___")
            self.show_cryptos(results["crypto"])

    def ad_hoc_plot(self, results):
        self.plot_company_ad_hoc(results)
        self.plot_price_ad_hoc(results)
        self.plot_news_ad_hoc(results)
        self.plot_crypto_ad_hoc(results)

    def ad_hoc_form(self, symbols):
        company_fields = ("symbol", "name", "exchange", "industry", "website", "description", "CEO", "sector",
                          "employees", "state", "city", "country", "logo")
        news_fields = ("symbol", "date", "title", "source", "url", "description", "image")
        ad_hoc = self.default_ad_hoc()

        self.st.markdown("___")
        self.st.markdown(f"**Company Options:**")
        cols = self.st.beta_columns([2, 1, 1])
        cols[0].markdown(f"**Specific company views:**")
        ad_hoc["company"]["specific"]["company_list"] = cols[0].multiselect("Stocks list:", sum(symbols, []))
        ad_hoc["company"]["specific"]["fields"] = cols[0].multiselect("Information:", company_fields)
        filter_cols = self.st.beta_columns(6)
        ad_hoc["company"]["specific"]["order_by"] = filter_cols[0].selectbox("Order By:", ad_hoc["company"]["specific"]["fields"]),
        ad_hoc["company"]["specific"]["order_method"] = filter_cols[1].selectbox("Order Method:", ("Ascending", "Descending")),
        ad_hoc["company"]["specific"]["limit"] = filter_cols[2].number_input("Number of results:", value=1, min_value=1, max_value=100),
        ad_hoc["company"]["specific"]["rule_filter"] = {}
        cols[1].markdown(f"**Insights views:**")
        cols[2].markdown(f"**-**")
        cols[1].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["company"]["insights"]["highest_emp"] = cols[1].checkbox("Highest employees number")
        cols[1].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["company"]["insights"]["tech"] = cols[1].checkbox("Information Companies")
        cols[2].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["company"]["insights"]["not_us"] = cols[2].checkbox("Outside USA")
        cols[2].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["company"]["specific"]["rule_filter"]["apply"] = cols[2].checkbox("Rule filter")
        if ad_hoc["company"]["specific"]["rule_filter"]["apply"]:
            ad_hoc["company"]["specific"]["rule_filter"]["field"] = filter_cols[0].selectbox(
                "Filter Field:", ("symbol", "name", "employees"))
            ad_hoc["company"]["specific"]["rule_filter"]["operation"] = filter_cols[1].selectbox(
                "Operation", ("Greater than", "Less than", "Equals to") if
                ad_hoc["company"]["specific"]["rule_filter"]["field"] == "employees" else ("Equals to", ))
            ad_hoc["company"]["specific"]["rule_filter"]["value"] = filter_cols[2].number_input("Value: ") \
                if ad_hoc["company"]["specific"]["rule_filter"]["field"] == "employees"\
                else filter_cols[2].text_input("Value: ")
        self.st.markdown("___")

        self.st.markdown(f"**Prices Options:**")
        price_cols = self.st.beta_columns([2, 1, 1])
        price_cols[0].markdown(f"**Specific price views:**")
        ad_hoc["price"]["specific"]["company_list"] = price_cols[0].multiselect("Price Stocks:", sum(symbols, []))
        filter_price_cols = self.st.beta_columns(6)
        ad_hoc["price"]["specific"]["start_date"] = filter_price_cols[0].date_input("Start Date:")
        ad_hoc["price"]["specific"]["end_date"] = filter_price_cols[1].date_input("End Date:")
        ad_hoc["price"]["specific"]["type"] = filter_price_cols[2].selectbox("Price Type:", ("close", "open", "high", "low")),
        price_cols[1].markdown(f"**Insights views:**")
        price_cols[2].markdown(f"**-**")
        price_cols[1].markdown("<br>", unsafe_allow_html=True)
        price_cols[2].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["price"]["insights"]["highest_close"] = price_cols[1].checkbox("Highest close price")
        price_cols[1].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["price"]["insights"]["lowest_close"] = price_cols[2].checkbox("Lowest close price")
        ad_hoc["price"]["insights"]["highest_volume"] = price_cols[1].checkbox("Highest volume")
        price_cols[2].markdown("<br>", unsafe_allow_html=True)
        ad_hoc["price"]["insights"]["lowest_volume"] = price_cols[2].checkbox("Lowest volume")

        self.st.markdown("___")
        self.st.markdown(f"**News Options:**")
        news_cols = self.st.beta_columns([2, 1, 1, 1])
        news_cols[0].markdown(f"**Specific news views:**")
        news_cols[1].markdown("-<br>", unsafe_allow_html=True)
        news_cols[2].markdown("-<br>", unsafe_allow_html=True)
        news_cols[3].markdown("-<br>", unsafe_allow_html=True)
        ad_hoc["news"]["company_list"] = news_cols[0].multiselect("News Stocks:", sum(symbols, []))
        ad_hoc["news"]["fields"] = news_cols[0].multiselect("News Info:", news_fields)
        ad_hoc["news"]["date"] = news_cols[1].date_input("Date:")
        ad_hoc["news"]["filter_date"] = news_cols[2].selectbox("Filter Date as:", ("On", "Starting from", "Until"))
        ad_hoc["news"]["order_by"] = news_cols[1].selectbox("Order by field:", ad_hoc["news"]["fields"])
        ad_hoc["news"]["order_method"] = news_cols[2].selectbox("Order results:", ("Ascending", "Descending"))
        ad_hoc["news"]["limit"] = news_cols[3].number_input("Limit of results:", value=1, min_value=1, max_value=100)
        ad_hoc["news"]["latest"] = news_cols[3].checkbox("Latest News")

        self.st.markdown("___")
        self.st.markdown(f"**Crypto Options:**")
        crypto_col = self.st.beta_columns([2, 0.5, 1])
        ad_hoc["crypto"]["name"] = crypto_col[0].text_input("Cryptocurrency")
        ad_hoc["crypto"]["limit"] = crypto_col[1].number_input("Limit of crypto:", value=1, min_value=1, max_value=100)

        generate = self.st.button("Generate Report")
        if generate:
            return ad_hoc

    @staticmethod
    def default_ad_hoc():
        return {
            "company": {
                "specific": {
                    "company_list": [],
                    "fields": [],
                    "order_by": None,
                    "order_method": None,
                    "limit": None,
                    "rule_filter": {
                        "apply": False,
                        "field": None,
                        "operation": None,
                        "value": None
                    }
                },
                "insights": {
                    "highest_emp": False,
                    "tech": False,
                    "not_us": False
                }
            },
            "news": {
                "company_list": [],
                "date": None,
                "filter_date": None,
            },
            "price": {
                "specific": {
                    "company_list": [],
                    "type": None,
                    "start_date": None,
                    "end_date": None
                },
                "insights": {
                    "highest_close": False,
                    "lowest_close": False,
                    "highest_volume": False,
                    "lowest_volume": False,
                }
            },
            "crypto": {
                "name": None,
                "limit": None
            }
        }