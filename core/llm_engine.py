import os
from core.retriever import search_financial_products
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from core.prompts import PB_SYSTEM_PROMPT

load_dotenv()

def generate_response(user_query: str, user_profile: dict) -> str:
    retrieved_context = search_financial_products(user_query, k =3)

    age = user_profile['cust_age']
    income = user_profile['cust_income']
    funds = user_profile['cust_funds']
    risk = user_profile['cust_risk']

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)



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
            "question": user_query
        })
        return response.content
    except Exception as e:
        return f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다: {e}"
    