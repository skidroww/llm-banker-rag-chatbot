import streamlit as st
from ui.sidebar import render_sidebar
from ui.chat_page import render_chat_page
import uuid

class App:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

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

