import os
from core.retriever import search_financial_products
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def generate_mock_response(user_query: str, user_profile: dict) -> str:

    retrieved_context = search_financial_products(user_query, k = 2)
    
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

def generate_response(user_query: str, user_profile: dict) -> str:
    retrieved_context = search_financial_products(user_query, k =3)

    age = user_profile.get('cust_age', 30)
    income = user_profile.get('cust_income', 300)
    funds = user_profile.get('cust_funds', 1000)
    risk = user_profile.get('cust_risk', '중도형')

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

    system_prompt = """당신은 하나은행의 전문 프라이빗 뱅커(PB) AI인 'FinRAG Advisor'입니다.
다음 제공되는 [고객 프로필]과 [검색된 상품 약관 정보]를 바탕으로 고객의 질문에 가장 적합한 금융 상품을 추천하고, 그 이유를 논리적이고 친절하게 설명해주세요.

[고객 프로필]
- 나이: {age}세
- 월 소득: {income}만원
- 여유/투자 자금: {funds}만원
- 투자 성향: {risk}

[검색된 상품 약관 정보]
{context}

[답변 지침]
1. [검색된 상품 약관 정보]에 없는 내용은 절대 지어내지 마세요 (환각 현상 엄격히 금지).
2. 추천하는 상품명과 함께, 고객의 프로필(투자 성향, 자금 등)과 연결지어 왜 이 상품이 고객님께 적합한지 논리적으로 설명하세요.
3. 약관에 금리나 가입 조건(기간, 최저가입금액 등)이 명시되어 있다면 수치를 포함하여 신뢰감 있게 안내하세요.
4. 친절하고 전문적인 은행원의 말투로 답변을 구성하세요.
"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    chain = prompt_template | llm

    try:
        response = chain.invoke({
            "age": age,
            "income": income,
            "funds": funds,
            "risk": risk,
            "context": retrieved_context,
            "question": user_query
        })
        return response.content
    except Exception as e:
        return f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다: {e}"
    