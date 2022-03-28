import streamlit as st
import plotly.express as px
import pandas as pd
from googletrans import Translator, constants

#################
# Translation
if "language" not in st.session_state:
    st.session_state["language"] = "English"

languages = { 'English': 'en', 'Spanish': 'es' }

@st.experimental_memo
def t(text_input):
    translator = Translator()
    translation = translator.translate(text_input, dest=languages[st.session_state["language"]])
    return translation.text

#################


def stats_page(rows):
    st.title(f":atom_symbol: {t('Quantum-Apps Hackathon')} :atom_symbol:")
    st.subheader(t("Take a look at the current teams!"))

    team_number = 0
    team_members = []
    team_size = []
    team_hist = {1: 0, 2: 0, 3: 0, 4: 0}
    category = {
        "Quantum Phenomena": 0,
        "Water care and food sustainability": 0,
        "Visualization and management of data for the conservation of the environment": 0,
        "Use of artificial intelligence and data science in Chemistry": 0,
        "Fight emerging diseases": 0,
        "Chemistry teaching": 0,
    }
    for row in rows:
        team_number += 1
        team_size.append(len(row.Participants.split(",")))
        team_hist[team_size[-1]] += 1
        category[row.Category] += 1
        # st.write(row)

    st.write(f"**{t('There are currently')} {team_number} {t('teams participating')}!** :tada:")
    st.write(t("Lets take a look at some of the statistics of the teams participating!"))

    st.subheader(t("Distribution of Teams:"))

    team_hist_list = list(team_hist.items())
    df_team_hist = pd.DataFrame(
        team_hist_list, columns=[t("Number of Participants per Team"), t("Count")]
    )
    fig = px.bar(df_team_hist, x=t("Number of Participants per Team"), y=t("Count"))
    st.plotly_chart(fig)

    st.subheader(t("Teams per Category:"))
    category_list = list(category.items())
    df_category = pd.DataFrame(category_list, columns=[t("Category"), t("Number of Teams")])
    fig = px.bar(df_category, x=t("Category"), y=t("Number of Teams"))
    st.plotly_chart(fig)
