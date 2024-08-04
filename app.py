import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
from datetime import datetime
import time
from tabs import calendario, upload_docs, substitute,  crea, segreteria, chiedi_seg



# streamlit_app.py

import hmac
import streamlit as st


from streamlit_cookies_manager import EncryptedCookieManager

from streamlit_js_eval import streamlit_js_eval



if 'login' not in st.query_params.keys():

    data_df = pd.read_csv("info_scuola.csv")
    info_scuola = data_df['info_scuola'][0]


    st.title("LEEM Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Quali sono gli orari?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chiedi_seg(prompt, info_scuola, str(st.session_state.messages))
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


else:



    # This should be a long random string
    COOKIE_SECRET = "your_cookie_secret_key"

    # Initialize the cookie manager
    cookies = EncryptedCookieManager(password=COOKIE_SECRET)

    if not cookies.ready():
        st.stop()

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
                cookies["username"] = st.session_state["username"]
                cookies["password_correct"] = "true"
                del st.session_state["password"]  # Don't store the username or password.
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        # Check if cookies have valid login information
        if cookies.get("password_correct") == "true":
            st.session_state["password_correct"] = True
            st.session_state["username"] = cookies.get("username")

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


    if st.button("Esci"):
        cookies["password_correct"] = "false"
        st.session_state.pop("password_correct")
        cookies["username"] = ''
        st.rerun()
    # try:
    #     usnm = cookies.get("username")
    # except:
    #     usnm = "None"
    # # Your main app code goes here
    # st.write(f"Ciao!")




    st.title("LEEM")

    # Create the tabs
    tab0, tab1, tab2, tab3, tab4 = st.tabs([ "Circolari", "Chatbot segreteria", "Calendario", "Ricerca supplemente", "Crea"])



    # Content for each tab
    with tab0:
        upload_docs()
        
    with tab1:
        segreteria()
    
    with tab2:
        calendario()

    with tab3:
        substitute()

    with tab4:
        crea()


