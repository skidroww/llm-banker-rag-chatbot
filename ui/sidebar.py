import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🏦 FinRAG Advisor")
        st.markdown(f"👤 **{st.session_state.get('username', 'PB')}**님, 환영합니다.")
        
        st.divider()
        
        st.subheader("🎯 가상 고객 프로필 설정")
        st.caption("LLM이 아래 정보를 바탕으로 맞춤형 상품을 추천합니다.")

        # 💡 알아서 추가한 부분: 포폴 시연용 퀵 프리셋 (페르소나)
        preset = st.selectbox(
            "👥 빠른 프로필 프리셋 (시연용)",
            ["직접 입력", "사회초년생 (안정추구형)", "30대 직장인 (수익추구형)", "은퇴 준비자 (원금보장형)"]
        )

        # 프리셋에 따른 기본값 세팅 로직
        default_age = 30
        default_income = 300
        default_funds = 1000
        default_risk = "중도형"

        if preset == "사회초년생 (안정추구형)":
            default_age, default_income, default_funds, default_risk = 26, 250, 500, "안정형"
        elif preset == "30대 직장인 (수익추구형)":
            default_age, default_income, default_funds, default_risk = 34, 400, 3000, "공격형"
        elif preset == "은퇴 준비자 (원금보장형)":
            default_age, default_income, default_funds, default_risk = 58, 500, 15000, "안정형"

        # 프로필 입력 폼
        st.session_state['cust_age'] = st.number_input("나이", min_value=20, max_value=100, value=default_age)
        st.session_state['cust_income'] = st.slider("월 소득 (만원)", 100, 2000, default_income, step=50)
        st.session_state['cust_funds'] = st.slider("여유/투자 가능 자금 (만원)", 100, 50000, default_funds, step=100)
        st.session_state['cust_risk'] = st.select_slider(
            "투자 성향", 
            options=["안정형", "중도형", "공격형"], 
            value=default_risk
        )
        
        st.divider()
        
        if st.button("로그아웃", type="secondary", use_container_width=True):
            st.session_state['is_logged_in'] = False
            st.rerun()