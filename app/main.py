

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

    def client_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Minha carteira", ))

    def advisor_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Cliente", "Carteiras", "Research"))

    def admin_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Carga de dados", "Advisors", "Relatório"))
        execute = False
        arg = None

        self.st.title("Stocker Administration Area")
        self.st.markdown("___")

        if option == "Carga de dados":
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

        elif option == "Relatório":
            self.st.header("Relatório")

        elif option == "Advisors":
            sub_option = self.st.selectbox("Opções:", ("Listar Advisors", "Registrar Advisor", "Editar Advisor"))
            self.st.markdown("___")
            if sub_option == "Listar Advisors":
                option = sub_option
                execute = True
            elif sub_option == "Registrar Advisor":
                arg = self.advisor_form(None)
                option = sub_option
                if arg:
                    execute = True
            elif sub_option == "Editar Advisor":
                arg = self.st.text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12")
                execute = True
                option = sub_option
                self.st.markdown("___")
        return option, execute, arg

    def advisor_form(self, advisor):
        cols = self.st.beta_columns([0.5, 0.25, 0.25])
        button = "Atualizar Advisor" if advisor else "Registrar Advisor"
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

