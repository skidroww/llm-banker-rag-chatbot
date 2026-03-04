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
        # DB
        try:
            self.conn = get_db()
        except Exception as e:
            print(e)
            self.conn = None
            print("db연결 실패")

        # 세션 상태 초기화 (로그인 상태 관리)
        if 'is_logged_in' not in st.session_state:
            st.session_state['is_logged_in'] = False
        if 'username' not in st.session_state:
            st.session_state['username'] = "User"

        

    def run(self):
        if not st.session_state['is_logged_in']:
            render_login_page(self.conn)
        else:
            render_sidebar()
            render_chat_page()

