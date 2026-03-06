import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings



load_dotenv()   

def clean_text(text: str) -> str:
    """
    안전한 전처리: 실제 약관 내용(영업점, 인터넷 등)이 훼손되지 않도록 
    확실한 노이즈(날짜, URL, 네비게이션)만 제거합니다.
    """
    # 1. 날짜/시간 관련 노이즈 완벽 제거
    text = re.sub(r'\d{2,4}\.\s*\d{1,2}\.\s*\d{1,2}\.\s*(오전|오후)\s*\d{1,2}:\d{2}', '', text)
    text = re.sub(r'\(\d{4}\.\d{2}\.\d{2}\s*기준\)?', '', text)
    text = re.sub(r'기준일자\s*:\s*\d{4}-\d{2}-\d{2}', '', text)

    # 2. 확실한 웹 UI 및 네비게이션 텍스트만 제거 ('영업점', '인터넷' 등은 내용 훼손 방지를 위해 제외)
    ui_keywords = [
        r'인쇄\s*\(\s*팝업\s*\)\s*<\s*KEB\s*하나은행', r'인쇄\s*취소',
        r'Home>예금>상품&가입', r'페이스북 공유하기 트위터 공유하기 관심상품추가 프린트하기 확대, 축소'
    ]
    for keyword in ui_keywords:
        text = re.sub(keyword, '', text)
    
    # 3. URL 주소 및 페이지 번호 제거
    text = re.sub(r'https?://[^\s]+', '', text)
    text = re.sub(r'\b\d+/\d+\b', '', text)
    
    # 4. 줄바꿈 및 다중 공백 정리 (LLM이 문맥을 잘 이해하도록)
    text = text.replace('\n', ' ')
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

    print("2.2 문맥 단절(Context Loss)방지를 위한 메타데이터 주입")
    for chunk in chunks:
        file_name = os.path.basename(chunk.metadata.get('source','')).replace('.pdf', '')

        chunk.page_content = f"[해당 상품명: {file_name}]\n{chunk.page_content}"

    print("3. Vector DB(Chroma)에 저장합니다")
    #embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")

    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="db")
    print("Vector DB 구축이 완료되었습니다.")
    return vectorstore

if __name__ == "__main__":
    build_vector_db()


