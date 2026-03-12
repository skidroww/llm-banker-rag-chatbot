import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🏦 FinRAG Advisor")
        st.markdown("👤 **고객 맞춤형 PB 챗봇**")
        
        st.divider()
        
        st.subheader("🎯 고객 프로필 설정")
        st.caption("이 정보들을 머신러닝 모델이 분석하여 고객의 금융 성향을 우선 진단합니다")

        preset = st.selectbox(
            "👥 빠른 고객 프로필 로드",
            [
                "직접 입력", 
                "사회초년생 (20대/미혼/소액자산)", 
                "20대 영끌 신혼부부 (기혼/주담대+신용대출)",
                "30대 전세거주 직장인 (미혼/신용대출)",
                "40대 중견 직장인 (기혼/주담대보유)", 
                "50대 자영업자 (기혼/여유자금)",
                "금수저 대학생 (20대/미혼/고액자산)",
                "은퇴자 (기혼/여유자금보유)",
                "생계형 은퇴자 (이혼/소액잔고/신용대출)"
            ]
        )

        #  기본값 세팅 
        default_age, default_job, default_marital, default_balance, default_housing, default_loan = 30, "사무직", "미혼", 1000, "아니오", "아니오"

        if preset == "사회초년생 (20대/미혼/소액자산)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 26, "사무직", "미혼", 300, "아니오", "아니오"
        elif preset == "20대 영끌 신혼부부 (기혼/주담대+신용대출)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 29, "기술직", "기혼", 150, "예", "예"
        elif preset == "30대 전세거주 직장인 (미혼/신용대출)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 34, "관리직", "미혼", 800, "아니오", "예"
        elif preset == "40대 중견 직장인 (기혼/주담대보유)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 45, "생산직", "기혼", 450, "예", "아니오"
        elif preset == "50대 자영업자 (기혼/여유자금)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 54, "자영업자", "기혼", 12000, "아니오", "아니오"
        elif preset == "금수저 대학생 (20대/미혼/고액자산)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 22, "학생", "미혼", 9500, "아니오", "아니오"
        elif preset == "은퇴자 (기혼/여유자금보유)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 68, "은퇴자", "기혼", 8500, "아니오", "아니오"
        elif preset == "생계형 은퇴자 (이혼/소액잔고/신용대출)":
            default_age, default_job, default_marital, default_balance, default_housing, default_loan = 72, "은퇴자", "이혼", 50, "아니오", "예"



        st.markdown("#### 👤 기본 프로필")
        # st.session_state에 저장해야 나중에 메인 앱(app.py)에서 ML 모델로 넘길 수 있음
        st.session_state['cust_age'] = st.number_input("연령", min_value=20, max_value=100, value=default_age)
        
        jobs = ['사무직', '기술직', '서비스직', '관리직', '은퇴자', '생산직', '무직', '개인사업자', '가사도우미', '알수없음', '자영업자', '학생']
        st.session_state['cust_job'] = st.selectbox("직업", options=jobs, index=jobs.index(default_job))
        
        maritals = ['기혼', '미혼', '이혼']
        st.session_state['cust_marital'] = st.selectbox("결혼상태", options=maritals, index=maritals.index(default_marital))
        
        st.markdown("#### 💰 금융/자산 정보")
        st.session_state['cust_balance'] = st.number_input("연간평균잔고 (단위: ₩)", value=default_balance, step=100)
        
        yes_no = ['예', '아니오']
        st.session_state['cust_housing'] = st.radio("주택담보대출여부", options=yes_no, index=yes_no.index(default_housing), horizontal=True)
        st.session_state['cust_loan'] = st.radio("개인신용대출여부", options=yes_no, index=yes_no.index(default_loan), horizontal=True)
        
        st.divider()
        
        
        