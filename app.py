import streamlit as st
from utils.db import get_db
from ui.login_page import render_login_page
from ui.sidebar import render_sidebar
from ui.chat_page import render_chat_page

class App:
    def __init__(self):

        st.set_page_config(
            page_title="FinRAG Advisor",
            page_icon="🏦",
            layout="wide",
            #initial_sidebar_state="collapsed"
            initial_sidebar_state="expanded"
        )
       
 
    
    def run(self):
            render_sidebar()
            render_chat_page()

