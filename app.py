import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
from datetime import datetime
import time
from tabs import calendario, upload_docs, search_docs, substitute, orari_profs, cerca_circ

# streamlit_app.py

import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()



st.title("LIM2")

# Create the tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Calendario", "Carica Circolari", "Ricerca Circolari", "Ricerca supplemente", "Orari", "Ricerca"])

# Content for each tab
with tab1:
  calendario()

with tab2:
   upload_docs()

with tab3:
   search_docs()

with tab4:
   substitute()

with tab5:
   orari_profs()

with tab6:
   cerca_circ()

