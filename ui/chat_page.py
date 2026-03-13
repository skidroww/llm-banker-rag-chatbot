import streamlit as st
import time
import pandas as pd
from catboost import CatBoostClassifier
from core.llm_engine import generate_response
import plotly.graph_objects as go

@st.cache_resource
def load_ml_model():
    model = CatBoostClassifier()
    model.load_model("./model/catboost_bank_model.cbm")
    return model

def create_gauge_chart(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        title={'text': "예치 성향", 'font': {'size': 18}},
        number={'suffix': "%", 'font': {'size': 36, 'color': '#1E3A8A'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2563EB"}, # 파란색 바
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#FEE2E2"},   # 빨간색 배경 (낮음)
                {'range': [30, 70], 'color': "#FEF3C7"},   # 노란색 배경 (중간)
                {'range': [70, 100], 'color': "#D1FAE5"}   # 초록색 배경 (높음)
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': probability
            }
        }
    ))
    # 차트 여백 최적화
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def render_chat_page():
    st.markdown("### 🏦 FinRAG PB 전문가용 대시보드")
    st.caption("AI 고객 성향 분석 리포트 및 RAG 기반 맞춤형 상품 추천 시스템")
    st.divider()

    ml_model = load_ml_model()

    user_profile = {
        '연령': st.session_state.get('cust_age', 30),
        '직업': st.session_state.get('cust_job', '사무직'),
        '결혼상태': st.session_state.get('cust_marital', '미혼'),
        '연간평균잔고': st.session_state.get('cust_balance', 1000),
        '주택담보대출여부': st.session_state.get('cust_housing', '아니오'),
        '개인신용대출여부': st.session_state.get('cust_loan', '아니오')
    }

    df_profile = pd.DataFrame([user_profile])
    deposit_prob = ml_model.predict_proba(df_profile)[0][1] * 100 #ml predic

    st.header("💬 하나은행 맞춤형 금융상품 추천 챗봇")
    st.caption("고객의 프로필과 하나은행 상품 약관(Vector DB)을 기반으로 최적의 상품을 추천합니다.")
    user_profile['예치성향점수'] = f"{deposit_prob:.1f}%"

    col1, col2 = st.columns([4, 6])

    # [왼쪽 화면] AI 고객 진단 리포트 (ML 결과 시각화)
    with col1:
        st.subheader("📊 AI 고객 성향 진단")
        st.markdown(f"**조회된 고객:** `{user_profile['연령']}세` | `{user_profile['직업']}` | `{user_profile['결혼상태']}`")
        
        #  Plotly 게이지 차트 렌더링
        fig = create_gauge_chart(deposit_prob)
        st.plotly_chart(fig, use_container_width=True)
        
        # AI 분석 코멘트 자동 생성
        st.markdown("💡 **AI 진단 요약**")
        if deposit_prob >= 70:
            st.success("🟢 **[VIP 타겟]** 여유 자금 예치 성향이 매우 높습니다.\n고금리 정기예금 및 VIP 특화 상품 추천을 제안합니다.")
        elif deposit_prob >= 40:
            st.warning("🟡 **[일반 타겟]** 안정적인 재테크 및 하이브리드 예적금 상품 위주의 접근이 필요합니다.")
        else:
            st.error("🔴 **[대출/소액 타겟]** 현재 자금 예치 여력이 낮을 확률이 높습니다.\n소액 짠테크 적금이나 대환 대출 상품을 안내하세요.")
            
        # 하단 자산 요약
        st.info(f"💰 **자산 및 부채 현황**\n- 연간평균잔고: **{user_profile['연간평균잔고']:,} 원**\n- 주택담보대출: **{user_profile['주택담보대출여부']}**\n- 개인신용대출: **{user_profile['개인신용대출여부']}**")


    # [오른쪽 화면] RAG 기반 PB 챗봇

    with col2:
        st.subheader("💬 맞춤형 PB 상담 챗봇")

        if "message" not in st.session_state:
            st.session_state.messages = []
            st.session_state["messages"] = [
                {"role": "assistant", "content": "안녕하세요! 하나은행 프라이빗 뱅커(PB) AI입니다. 좌측에 설정된 고객 프로필을 바탕으로 어떤 금융 상품을 알아보고 싶으신가요?"}
            ]

        chat_container = st.container(height=500)

        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    
        if prompt := st.chat_input("예:여유 자금이 있는데 금리 높은 예금 추천해줘"):
            # 1. 사용자 질문을 화면에 표시 및 저장
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

        
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("상품 약관을 검색하고 고객 프로필을 분석 중입니다..."):
                    time.sleep(0.1) 

                    message_placeholder.markdown(f"*(📊 ML AI 진단: 고객님의 여유자금 예치 성향은 **{deposit_prob:.1f}%** 입니다. 이를 반영하여 답변을 작성합니다...)*")
                    time.sleep(0.1)

                    final_response = generate_response(prompt, user_profile, st.session_state.messages)

                    displayed_text = ""
                    for chunk in final_response.split('\n'):
                        displayed_text += chunk + "\n"
                        message_placeholder.markdown(displayed_text + "▌")
                        time.sleep(0.05)
                    
                    message_placeholder.markdown(displayed_text)
                    
            # 3. AI 답변을 세션에 저장
            st.session_state.messages.append({"role": "assistant", "content": final_response})

               


                

