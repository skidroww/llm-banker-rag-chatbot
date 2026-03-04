import streamlit as st
import time

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
            
            # TODO: Phase 3에서 아래 부분을 실제 RAG 검색(retriever) + LLM 생성 코드로 교체합니다.
            # 지금은 UI 테스트를 위해 가짜 응답(Loading)을 보여줍니다.
            with st.spinner("상품 약관을 검색하고 고객 프로필을 분석 중입니다..."):
                time.sleep(1.5) # 가짜 딜레이
                
                # 테스트용 임시 답변 (고객 프로필 데이터가 잘 연동되는지 확인용)
                profile_summary = f"({st.session_state['cust_age']}세, 월소득 {st.session_state['cust_income']}만원, {st.session_state['cust_risk']} 성향)"
                mock_response = f"고객님의 {profile_summary}을 반영하여 검색한 결과입니다.\n\n안전하게 목돈을 굴리시려면 **'고단위 플러스(금리확정형)'** 상품을 추천합니다. Vector DB 검색 결과, 이 상품은...\n\n(※ 이 부분은 추후 LLM 실제 응답으로 대체됩니다.)"
                
                message_placeholder.markdown(mock_response)
                
        # 3. AI 답변을 세션에 저장
        st.session_state.messages.append({"role": "assistant", "content": mock_response})

