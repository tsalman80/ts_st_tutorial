import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# hashed_passwords = stauth.Hasher.hash_passwords(config["credentials"])
# print(hashed_passwords)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

st.session_state["authenticator"] = authenticator


try:
    authenticator.login()
except Exception as e:
    print(e)

if st.session_state["authentication_status"]:
    print(st.session_state)
    st.switch_page("pages/home.py")
    # st.write("Hello")
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
