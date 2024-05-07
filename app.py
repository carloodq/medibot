import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
import pandas as pd
from datetime import datetime
import time
from tabs import calendario, upload_docs, search_docs, substitute, orari_profs, cerca_circ


st.title("App Gestionale Liceo Medi")

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

