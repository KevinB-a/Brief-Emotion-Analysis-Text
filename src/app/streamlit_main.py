import sys
sys.path.insert(0,'/home/apprenant/Documents/Brief-Emotion-Analysis-Text')
import streamlit as st
from src.app import app1
from src.app import app2 

PAGES = {
    "App1": app1,
    "App2": app2
        }
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()