import streamlit as st
from PIL import Image
import os
from googletrans import Translator, constants

#################
# Translation
if "language" not in st.session_state:
    st.session_state["language"] = "English"

languages = {"English": "en", "Spanish": "es"}


def t(text_input):
    translator = Translator()
    translation = translator.translate(
        text_input, dest=languages[st.session_state["language"]]
    )
    return translation.text


# st.write('home.py - ', st.session_state["language"])
#################


def home_page(rows):
    st.title(f":atom_symbol: {t('Quantum-Apps Hackathon')} :atom_symbol:")

    st.markdown(
        f"{t('This hackathon is aimed at students of the Faculty of Chemical Sciences of the Autonomous University of Chihuahua, but also at students of related areas in other faculties of the same university.')}"
    )

    st.markdown(f"### :books: {t('Requirements')}:")
    st.markdown(
        f"- {t('Enrolled students or recent graduates (no more than six months after graduation) may participate.')}"
    )
    st.markdown(f"- {t('Register by filling out the fields on this page.')}")

    st.markdown(f"### :1234: {t('Rules')}:")
    st.markdown(f"- {t('Teams of up to 4 contestants are allowed.')}")
    st.markdown(f"- {t('The same person cannot be in more than one team.')}")
    st.markdown(
        f"- {t('Participants can have a mentor (optional), who must be registered.')}"
    )
    st.markdown(
        f"- {t('Each Team needs a unique name and password that all the team members know and have access to. The Team name and password will be used to enter, modify and submit the hackathon project.')}"
    )

    st.markdown(f"### {t('Organizers')}:")
    st.image(Image.open("images/organizer.png"))
