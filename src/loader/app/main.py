import streamlit as st
from src.loader.app.data_load import loader

side_bar = st.sidebar
st.set_page_config(layout='wide')


class Streamlit:

    def __init__(self):
        _user = side_bar.text_input("Username:")
        _pass = side_bar.text_input("Password", type="password")
        profile = self.get_profile(_user, _pass)
        self.layout_config(profile)

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

    @staticmethod
    def show_message(_type, message):
        if _type == "success":
            st.success(message)
        elif _type == "error":
            st.error(message)
        elif _type == "warning":
            st.error(message)

    def client_setup(self):
        option = side_bar.selectbox("Opções:", ("Minha carteira", ))

    def advisor_setup(self):
        option = side_bar.selectbox("Opções:", ("Cliente", "Carteiras", "Research"))

    def admin_setup(self):
        option = side_bar.selectbox("Opções:", ("Relatório", "Carga de dados"))
        st.title("Stocker Administration Area")
        st.markdown("___")

        if option == "Carga de dados":
            self.show_message("warning", "Atenção! A carga de dados fará todos os requests na API "
                                         "para carregar o banco de dados (Pontos)")

            if st.button("Carga de dados"):
                with st.spinner('Realizando carga de dados...'):
                    status = loader()
                    st.write(status)
                if status:
                    self.show_message("success", "Carga de dados realizada com sucesso!")
                else:
                    self.show_message("error", "Ocorreu um erro durante a relização da carga de dados!")


        if option == "Relatório":
            st.write("xz")

    def layout_config(self, profile):
        if profile:
            side_bar.info(f"Você agora está logado como {profile}")
            if profile == "admin":
                self.admin_setup()
            elif profile == "advisor":
                self.advisor_setup()
            elif profile == "client":
                self.client_setup()
        else:
            side_bar.error("Suas credenciais são inválidas")


Streamlit()