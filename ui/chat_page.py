import streamlit as st
import time
from core.llm_engine import generate_mock_response

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

    
    if prompt := st.chat_input("예: 1년 정도 굴릴 여유 자금이 있는데 금리 높은 예금 추천해줘"):
        # 1. 사용자 질문을 화면에 표시 및 저장
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. AI 답변 생성 (이 부분은 추후 core/llm_engine.py 연동 시 수정될 부분입니다)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            with st.spinner("상품 약관을 검색하고 고객 프로필을 분석 중입니다..."):
                time.sleep(1.0) # 가짜 딜레이


                user_profile = {
                    'cust_age': st.session_state.get('cust_age', 30),
                    'cust_income': st.session_state.get('cust_income', 300),
                    'cust_funds': st.session_state.get('cust_funds', 1000),
                    'cust_risk': st.session_state.get('cust_risk', '중도형')
                }

                final_response = generate_mock_response(prompt, user_profile)
                
                displayed_text = ""
                for chunk in final_response.split('\n'):
                    displayed_text += chunk + "\n"
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.05)
                
                message_placeholder.markdown(displayed_text)
                
        # 3. AI 답변을 세션에 저장
        st.session_state.messages.append({"role": "assistant", "content": final_response})

