import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report



# Demaragge avec l'environnement myenvs

st.title('Analyse de données')


file_path = 'donnees_stat.csv'
df = pd.read_csv(file_path)


if st.button('Générer le rapport de profil'):
    profile = ProfileReport(df, title=' Profiling Report')
    st_profile_report(profile)
