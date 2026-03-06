import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_retriever():
    print("⏳ Vector DB 및 임베딩 모델 로드 중...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
        BASSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASSE_DIR, "db")

        if not os.path.exists(db_path):
            print("❌ Vector DB 경로를 찾을 수 없습니다!")
            return None
        
        vector_db = Chroma(persist_directory=db_path,embedding_function=embeddings)
        print("✅ Vector DB 로드 완료!")
        return vector_db
    
    except Exception as e:
        print(f"❌ Vector DB 로드 중 오류 발생: {e}")
        return None


def search_financial_products(query: str, target_product:str, k: int = 10) -> str:
    vector_db = get_retriever()

    if vector_db is None:
        return "시스템 오류: 금융 상품 데이터베이스(Vector DB)를 불러올 수 없습니다."
    
    docs = vector_db.similarity_search(query, k=k)

    if target_product:
        target_clean = target_product.replace(" ", "")
        filtered_docs = []
        
        for doc in docs:
            source_file = doc.metadata.get('source', '')
            if target_clean in source_file.replace(" ", ""):
                filtered_docs.append(doc)
        
        if filtered_docs:
            docs = filtered_docs

    docs = docs[:k]

    if not docs:
        return "죄송합니다. 고객님의 질문과 관련된 금융 상품을 찾을 수 없습니다. 다른 질문을 해보시겠어요?"
    
    context_parts = []
    for i, doc in enumerate(docs):
        source_path = doc.metadata.get("source", "알 수 없는 출처")
        page = doc.metadata.get("page", "알 수 없는 페이지")
        file_name = os.path.basename(source_path)

        chunk_text = f"[{i+1}번 정보 출처: {file_name}(페이지:{page})]\n{doc.page_content}"
        context_parts.append(chunk_text)

    combined_context = "\n\n---\n\n".join(context_parts)
    return combined_context

