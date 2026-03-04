from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def check_my_db():
    print("1. 임베딩 모델 불러오는 중...")
    # DB를 만들 때 썼던 똑같은 무료 모델을 가져와야 해석할 수 있습니다.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("2. 로컬 DB(db/ 폴더) 연결 중...\n")
    # 저장해둔 db 폴더를 지정해서 Vector DB를 불러옵니다.
    vector_db = Chroma(
        persist_directory="db/", 
        embedding_function=embeddings
    )

    # 1. 총 몇 개의 조각(Chunk)이 저장되었는지 확인
    total_chunks = vector_db._collection.count()
    print(f"✅ 현재 DB에 저장된 텍스트 조각 개수: {total_chunks}개\n")

    if total_chunks == 0:
        print("앗, DB가 비어있습니다. rag_pipeline.py를 다시 실행해 보세요.")
        return

    # 2. 테스트용 검색 날려보기 (금리, 이자, 우대 등 원하는 단어로 바꿔보세요)
    test_query = "금리 우대 조건이 어떻게 돼?"
    print(f"🤖 테스트 질문: '{test_query}'")
    print("결과를 찾는 중...\n")
    
    # DB에서 질문과 가장 관련성 높은 2개의 조각을 가져옵니다.
    docs = vector_db.similarity_search(test_query, k=2)

    for i, doc in enumerate(docs):
        print(f"--- [검색 결과 {i+1}] ---")
        # 어떤 PDF의 몇 페이지에서 가져왔는지 출처 확인
        source = doc.metadata.get('source', '알 수 없음')
        page = doc.metadata.get('page', '알 수 없음')
        print(f"📑 출처: {source} (페이지: {page})")
        
        # 실제 내용 확인 (너무 기니까 200자만 출력)
        print(f"📝 내용: {doc.page_content[:200]}...\n")

if __name__ == "__main__":
    check_my_db()