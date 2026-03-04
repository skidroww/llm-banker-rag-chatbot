import streamlit as st
from utils.db import get_db
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.prediction import render_prediction_page
from ui.simulation import render_simulation_page
from ui.optimization import render_optimization_page
from ui.infra_page import render_infra_page
from ui.login_page import render_login_page

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
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "1"

        

    def run(self):
        if not st.session_state['is_logged_in']:
            render_login_page(self.conn)
        else:
            render_sidebar()
            # 페이지 라우팅
            page = st.session_state.current_page
            if page == "1":
                render_infra_page(self.conn)
            elif page == "2":
                render_dashboard()
            elif page == "3":
                render_prediction_page()
            elif page == "4":
                render_simulation_page()
            elif page == "5":
                render_optimization_page()

