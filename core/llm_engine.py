import time
from core.retriever import search_funancial_products

def generate_mock_response(user_query: str, user_profile: dict) -> str:
    retrieved_context = search_funancial_products(user_query, k = 2)
    
    age = user_profile.get('cust_age', 30)
    income = user_profile.get('cust_income', 300)
    funds = user_profile.get('cust_funds', 1000)
    risk = user_profile.get('cust_risk', '중도형')

    system_prompt = f"""
    당신은 하나은행의 전문 PB입니다.
    [고객 정보] 나이: {age}세, 월소득: {income}만원, 여유자금: {funds}만원, 투자성향: {risk}
    [검색된 상품 정보] 
    {retrieved_context}
    """
    # 콘솔(터미널)에 프롬프트가 어떻게 만들어졌는지 출력해봅니다 (디버깅용)
    print("========== [LLM에게 전달될 프롬프트] ==========")
    print(system_prompt)
    print("===============================================")
    

    mock_answer = f"""
**[안내: 현재 API 키 연동 전 가상 답변 모드입니다.]**

👤 **분석된 고객 프로필**: {age}세 / 월 {income}만원 소득 / {risk} 성향 / 가용자금 {funds}만원
🔍 **고객님의 질문**: "{user_query}"

위 정보를 바탕으로 하나은행 내부 상품 데이터베이스를 검색한 결과, 아래와 같은 약관 정보를 찾았습니다. 
(실제 LLM이 연결되면 이 정보를 바탕으로 자연스러운 추천 멘트를 작성하게 됩니다.)

---
**[Vector DB에서 찾은 참고 자료 요약]**
{retrieved_context}
---

💡 **추천 방향 (예시)**: 
고객님은 '{risk}' 성향이시므로, 위 검색된 상품 중 안정성을 보장하면서도... (나중에 LLM이 채워줄 영역입니다!)
"""
    return mock_answer