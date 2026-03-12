import streamlit as st
import time
import pandas as pd
from catboost import CatBoostClassifier
from core.llm_engine import generate_response

@st.cache_resource
def load_ml_model():
    model = CatBoostClassifier()
    model.load_model("./model/catboost_bank_model.cbm")
    return model


def render_chat_page():
    st.header("💬 하나은행 맞춤형 금융상품 추천 챗봇")
    st.caption("고객의 프로필과 하나은행 상품 약관(Vector DB)을 기반으로 최적의 상품을 추천합니다.")

    #if "messages" not in st.session_state:     
    #    st.session_state.messages = []

    if "message" not in st.session_state:
        st.session_state.messages = []
        st.session_state["message"] = [
            {"role": "assistant", "content": "안녕하세요! 하나은행 프라이빗 뱅커(PB) AI입니다. 좌측에 설정된 고객 프로필을 바탕으로 어떤 금융 상품을 알아보고 싶으신가요?"}
        ]

    for message in st.session_state.message:
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

                user_profile['예치성향점수'] = f"{deposit_prob:.1f}%"

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

