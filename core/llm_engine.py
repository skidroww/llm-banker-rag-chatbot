import os
from core.retriever import search_financial_products
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from core.prompts import PB_SYSTEM_PROMPT
import json
import re

load_dotenv()

def extract_text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content,list):
        return "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    if isinstance(content,dict):
        return content.get("text", str(content))
    return str(content)

def get_standalone_query(user_query: str, chat_history: list, llm) -> str:

    if len(chat_history) <=1:
        return user_query
    
    history_str = ""
    for msg in chat_history[-4:]:
        role = "PB" if msg["role"] == "assistant" else "고객"
        history_str += f"{role}: {msg['content']}\n"

    prompt = f"""이전 대화 기록을 참고하여, 고객의 마지막 질문을 문맥이 포함된 완벽하고 독립적인 하나의 문장으로 다시 작성해주세요.
만약 마지막 질문이 이미 독립적이고 명확하다면 그대로 반환하세요.
답변이나 인사를 덧붙이지 말고, 오직 '재작성된 질문' 텍스트만 반환하세요.

[이전 대화 기록]
{history_str}

[마지막 질문]
고객: {user_query}

[재작성된 질문]:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"질문 재작성 중 오류 발생: {e}")
        return user_query

def get_query_and_product(user_query: str, chat_history: list, llm) -> tuple:
    history_str = ""
    if len(chat_history) > 1:
        for msg in chat_history[-4:]:
            role = "PB" if msg["role"] == "assistant" else "고객"
            history_str += f"{role}: {msg['content']}\n"

    prompt = f"""당신은 대화 문맥을 파악하는 AI입니다.이전 대화 기록을 참고하여, 고객의 마지막 질문을 완벽한 하나의 문장으로 재작성하고, 고객이 특정 금융 상품을 지칭하고 있는지 파악하세요.
이전 대화 기록을 참고하여, 고객의 마지막 질문에 포함된 대명사('이거', '저 상품', '그거' 등)를 PB가 방금 추천하거나 언급한 구체적인 상품명으로 대체하여 완벽한 하나의 문장으로 재작성하세요.
또한, 대화 문맥상 고객이 묻고 있는 특정 금융 상품의 정확한 이름을 추출하세요.

[이전 대화 기록]
{history_str}

[마지막 질문]
고객: {user_query}

[출력 지침]
반드시 아래 JSON 형식으로만 응답하세요. 마크다운(```json 등)은 절대 포함하지 마세요.
{{
    "query": "재작성된 문장"(예: 3,6,9 정기예금 상품은 어떤 장점이 있나요?),
    "product": "대화에 등장한 타겟 상품명 (특정 상품을 지칭하지 않으면 \"\" 빈 문자열 기재)"
}}
"""
    try:
        response = llm.invoke(prompt)
        #text = response.content.strip()
        raw_text = extract_text_content(response.content).strip()

        #text = re.sub(r'```json\s*', '', text)
        #text = re.sub(r'```\s*', '', text)

        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result.get("query", user_query), result.get("product", "")
        return user_query, ""

        #result = json.loads(text)
        #return result.get("query", user_query), result.get("product", "")
    except Exception as e:
        print(f"질문/상품명 추출 실패: {e}")
        return user_query, ""

def generate_response(user_query: str, user_profile: dict, chat_history: list) -> str:
    #llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.2)

    standalone_query, target_product = get_query_and_product(user_query, chat_history, llm)

    deposit_prob = float(user_profile['예치성향점수'].replace('%', ''))
    age = user_profile['연령']

    if target_product:
        optimized_query = f"{target_product} 상품의 금리, 혜택, 가입 조건"
        print(f"optimized_query:{optimized_query}")
    else:
        if deposit_prob >= 70:
            optimized_query = f"목돈을 굴리기 좋은 고금리 거치식 정기예금 및 VIP 우대 상품 특징"
        elif deposit_prob < 40:
            optimized_query = f"여유 자금이 부족하거나 대출이 있는 고객을 위한 소액 적금, 짠테크 또는 대환 대출 상품"
        elif age >= 55:
            optimized_query = f"은퇴자 및 시니어를 위한 연금 예금, 노후 자금 관리 상품"
        else:
            optimized_query = standalone_query # 그 외에는 원래 질문 그대로 사용

    print(f"\n [추출 결과] 검색용 질문: '{standalone_query}'")
    print(f" [추출 결과] 타겟 상품명: '{target_product}'\n")
    print(f"\n [Query Rewriting] 원래 질문: '{user_query}'")
    print(f" [Query Rewriting] 검색용 질문: '{standalone_query}'\n")

    retrieved_context = search_financial_products(standalone_query, target_product=target_product, k=4)

    print("\n"+"="*70)
    print("[RAG 검색 결과] LLM에게 전달된 약관 원문(context)")
    print("="*70)
    print(retrieved_context)
    print("\n"+"="*70)

    profile_str = "\n".join([f"- {k}: {v}" for k, v in user_profile.items()])

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"{PB_SYSTEM_PROMPT}\n\n[현재 고객 AI 진단 프로필]\n{profile_str}"),
        ("human", "고객 질문: {question}\n\n[RAG 검색 약관 정보]\n{context}\n\n위 프로필과 약관을 바탕으로 답변해주세요.")
    ])

    chain = prompt_template | llm

    try:
        response = chain.invoke({
            "context": retrieved_context,
            "question": standalone_query
        })
        #return response.content
        return extract_text_content(response.content)
    except Exception as e:
        return f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다: {e}"
    