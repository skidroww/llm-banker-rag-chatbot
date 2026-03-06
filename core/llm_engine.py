import os
from core.retriever import search_financial_products
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from core.prompts import PB_SYSTEM_PROMPT

load_dotenv()

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


def generate_response(user_query: str, user_profile: dict, chat_history: list) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

    standalone_query = get_standalone_query(user_query, chat_history, llm)
    print(f"\n [Query Rewriting] 원래 질문: '{user_query}'")
    print(f" [Query Rewriting] 검색용 질문: '{standalone_query}'\n")

    retrieved_context = search_financial_products(standalone_query, k =10)

    age = user_profile['cust_age']
    income = user_profile['cust_income']
    funds = user_profile['cust_funds']
    risk = user_profile['cust_risk']

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", PB_SYSTEM_PROMPT),
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
            "question": standalone_query
        })
        return response.content
    except Exception as e:
        return f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다: {e}"
    