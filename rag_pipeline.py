import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings



load_dotenv()   


def build_vector_db():
    print("1. data 폴더에서 PDF 문서들을 읽어옵니다.")
    loader = PyPDFDirectoryLoader("./data")
    documents = loader.load()
    print(f"총 {len(documents)}개의 문서를 불러왔습니다.")

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


