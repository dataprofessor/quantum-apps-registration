import streamlit as st
from gsheetsdb import connect  # to connect and look at data
from google.oauth2 import service_account
import gspread  # to write data to the DB
import plotly.express as px
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(page_title="Quantum-Apps Hackathon", page_icon="⚛️")

from modules import home, register, submit, stats

#################
# Translation
from googletrans import Translator, constants

language_value = []
languages = {"English": "en", "Spanish": "es"}

if "language" not in st.session_state:
    st.session_state["language"] = "English"

if st.session_state["language"] == "English":
    language_value.append(0)
else:
    language_value.append(1)


selected_language = st.sidebar.selectbox(
    "Select a language", languages, index=language_value[0]
)
st.session_state["language"] = selected_language


def t(text_input):
    translator = Translator()
    translation = translator.translate(text_input, dest=languages[selected_language])
    return translation.text


# st.write('streamlit_app.py - ', f'selectbox: {selected_language}, ', f'Session state: {st.session_state["language"]}')

#################


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows


sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

if "team_chosen" not in st.session_state:
    st.session_state.team_chosen = False
    st.session_state.members = []
    st.session_state.mentor = ""
    st.session_state.category_index = 0

if "team" not in st.session_state:
    st.session_state["team"] = ""

if "pwd" not in st.session_state:
    st.session_state["pwd"] = ""

if "num_teams" not in st.session_state:
    st.session_state["num_teams"] = 1

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


title_to_app = {
    t("Home"): home.home_page,
    t("Register"): register.register_page,
    t("Submit"): submit.submit_page,
    t("Statistics"): stats.stats_page,
}

query_params = st.experimental_get_query_params()
if "page" in query_params:
    page_url = query_params["page"][0]
    if page_url in title_to_app.keys():
        st.session_state["page_selector"] = page_url


def change_page_url():
    st.experimental_set_query_params(page=st.session_state["page_selector"])


titles = list(title_to_app.keys())

selected_page = st.sidebar.radio(
    t("Pages:"),
    titles,
    key="page_selector",
    on_change=change_page_url,
)
title_to_app[selected_page](rows)
