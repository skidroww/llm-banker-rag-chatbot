import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings



load_dotenv()   

def clean_text(text: str):
    text = re.sub(r'\d{2,4}\.\s*\d{1,2}\.\s*\d{1,2}\.\s*(오전|오후)\s*\d{1,2}:\d{2}', '', text)
    # 예: "(2026.03.04 기준", "기준일자 : 2026-03-04"
    text = re.sub(r'\(\d{4}\.\d{2}\.\d{2}\s*기준\)?', '', text)
    text = re.sub(r'기준일자\s*:\s*\d{4}-\d{2}-\d{2}', '', text)

    # 2. 웹 UI 버튼 및 네비게이션 텍스트 제거
    ui_keywords = [
        r'인쇄\s*\(\s*팝업\s*\)\s*<\s*KEB\s*하나은행', r'인쇄\s*취소',
        r'Home>예금>상품&가입', r'페이스북 공유하기 트위터 공유하기 관심상품추가 프린트하기 확대, 축소',
        r'상담예약', r'영업점', r'인터넷', r'스마트폰', r'가입하기'
    ]
    for keyword in ui_keywords:
        text = re.sub(keyword, '', text)
    
    # 3. URL 주소 및 페이지 번호 제거
    text = re.sub(r'https?://[^\s]+', '', text)
    text = re.sub(r'\b\d+/\d+\b', '', text)
    
    # 4. PDF 파싱 시 발생하는 불필요한 줄바꿈을 공백으로 치환하여 문장 이어주기
    text = text.replace('\n', ' ')
    
    # 5. 다중 공백을 하나의 공백으로 깔끔하게 정리
    text = re.sub(r'\s{2,}', ' ', text)
    
    return text.strip()

def build_vector_db():
    print("1. data 폴더에서 PDF 문서들을 읽어옵니다.")
    loader = PyPDFDirectoryLoader("./data")
    documents = loader.load()
    print(f"총 {len(documents)}개의 문서를 불러왔습니다.")

    print("1-2. 문서 노이즈(헤더, 푸터 등) 전처리를 진행합니다.")
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    print("2. 문서를 적절한 크기로 쪼갭니다(chunk)")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # 1000글자 단위로 쪼개고, 문맥이 끊기지 않게 100글자씩 겹치게 설정

    chunks = text_splitter.split_documents(documents)
    print(f"총 {len(chunks)}개의 chunk로 분할되었습니다.")

    print("3. Vector DB(Chroma)에 저장합니다")
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="db")
    print("Vector DB 구축이 완료되었습니다.")
    return vectorstore

#if __name__ == "__main__":
#    build_vector_db()


