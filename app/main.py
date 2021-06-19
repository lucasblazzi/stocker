

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

    def login(self):
        _user = self.side_bar.text_input("Username:")
        _pass = self.side_bar.text_input("Password", type="password")
        return _user, _pass

    def client_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Minha carteira", ))

    def advisor_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Cliente", "Carteiras", "Research"))

    def admin_setup(self):
        option = self.side_bar.selectbox("Opções:", ("Relatório", "Carga de dados", "Advisors"))
        execute = False
        advisor = None

        self.st.title("Stocker Administration Area")
        self.st.markdown("___")

        if option == "Carga de dados":
            self.show_message("st", "warning", "Atenção! A carga de dados fará todos os requests na API "
                                               "para carregar o banco de dados (1.140.225 de créditos)")
            if self.st.button("Carga de dados"):
                execute = True
        elif option == "Relatório":
            self.st.write("xz")
            if self.st.button("Carga de dados"):
                execute = True
        elif option == "Advisors":
            sub_option = self.st.selectbox("Opções:", ("Listar Advisors", "Registrar Advisor", "Editar Advisor"))
            self.st.markdown("___")
            if sub_option == "Listar Advisors":
                option = sub_option
                execute = True
            elif sub_option == "Registrar Advisor":
                advisor = self.advisor_form(None)
                option = sub_option
                if advisor:
                    execute = True
            elif sub_option == "Editar Advisor":
                advisor = self.st.text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12")
                execute = True
                option = sub_option
                self.st.markdown("___")
        return option, execute, advisor

    def advisor_form(self, advisor):
        cols = self.st.beta_columns([0.5, 0.25, 0.25])
        advisor = {
            "name": cols[0].text_input("Nome", max_chars=30, type='default', help="Nome Completo",
                                       value=advisor["name"]) if advisor
            else cols[0].text_input("Nome", max_chars=30, type='default', help="Nome Completo"),

            "cpf": cols[1].text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12",
                                      value=advisor["cpf"]) if advisor
            else cols[1].text_input("CPF", max_chars=15, type='default', help="CPF: 123.123.123-12"),

            "cvm_license": cols[2].text_input("Lincença CVM", max_chars=10, type='default',
                                              value=advisor["cvm_license"]) if advisor
            else cols[2].text_input("Lincença CVM", max_chars=10, type='default'),

            "email": cols[0].text_input("Email", max_chars=30, type='default', value=advisor["email"]) if advisor
            else cols[0].text_input("Email", max_chars=30, type='default'),

            "username": cols[1].text_input("Usuário", max_chars=15, type='default', help="Usuário para login",
                                           value=advisor["username"]) if advisor
            else cols[1].text_input("Usuário", max_chars=15, type='default', help="Usuário para login"),

            "password": cols[2].text_input("Senha", max_chars=15, type='password', help="Senha para login",
                                           value=advisor["password"]) if advisor
            else cols[2].text_input("Senha", max_chars=15, type='password', help="Senha para login"),

            "profile": self.st.text_input("Profile", value="Advisor")
        }
        button = "Atualizar Advisor" if advisor else "Registrar Advisor"
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

