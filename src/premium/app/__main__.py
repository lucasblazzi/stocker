import streamlit as st


def is_authenticated(username, password):
    return username == "admin" and password == "admin"


def generate_login_block():
    block1 = st.empty()
    block2 = st.empty()
    block3 = st.empty()
    block4 = st.empty()
    return block1, block2, block3, block4


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def login(blocks):
    blocks[0].title("Stocker Permium Area")
    username_block = blocks[1].text_input("Username", type="default")
    pass_block = blocks[2].text_input("Password", type="password")
    login_block = blocks[3].button('Login')
    return username_block, pass_block, login_block


def main():
    st.balloons()


login_blocks = generate_login_block()
_user, _pass, login = login(login_blocks)

if login:
    if is_authenticated(_user, _pass):
        clean_blocks(login_blocks)
        main()
    else:
        st.error("Please provide valid credentials")