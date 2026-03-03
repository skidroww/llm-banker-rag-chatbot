# llm-banker-rag-chatbot
고객 프로필 기반 금융 상품 RAG 추천 시스템| FinRAG: Personalized Financial Product Recommendation Chatbot using LLM &amp; ChromaDB.


# 🏦 FinRAG Advisor: 생성형 AI 기반 맞춤형 금융 상품 추천 시스템
> **하나은행 생성형AI/AI모델링 직무 지원 포트폴리오**
> 제작 기간: 2026.03.XX ~ 2026.03.XX (10일)

## 1. Project Overview (프로젝트 개요)
- **기획 의도:** 복잡한 금융 약관과 상품 설명서를 LLM이 분석하고, 고객의 가상 프로필(소득, 성향)에 맞춰 최적의 상품을 논리적으로 추천하는 RAG 파이프라인 구축
- **핵심 목표:** 금융 도메인에서의 LLM 환각(Hallucination) 현상 제어 및 개인화된 설명 제공

## 2. Tech Stack (기술 스택)
- **Language:** Python
- **AI/ML:** LangChain, OpenAI API (GPT-4o-mini), HuggingFace Embeddings
- **Database:** ChromaDB (Vector Store)
- **Frontend:** Streamlit

## 3. System Architecture (시스템 구조)
- (여기에 나중에 데이터 수집 -> Vector DB -> LLM -> Streamlit 으로 이어지는 간단한 다이어그램 이미지 첨부)

## 4. Key Features (주요 기능)
- PDF/텍스트 기반 금융 상품 약관 Chunking 및 Vector DB 구축
- 고객 프로필(투자 성향, 목표 금액 등)을 반영한 맞춤형 프롬프트 엔지니어링
- 답변 출처(Source) 표기를 통한 신뢰성 확보

## 5. How to Run (실행 방법)


[Phase 1: 데이터 확보 및 전처리 (1~2일차)]

데이터 수집: 하나은행(또는 타행) 홈페이지에서 대표적인 예금, 적금, 대출 상품 설명서(PDF)나 약관 텍스트를 10~20개 정도 수집합니다.

가상 유저 데이터: "월 소득 300만 원, 보수적 투자 성향, 여유 자금 50만 원" 같은 가상 고객 프로필을 담은 간단한 CSV 파일을 만듭니다. (이게 핵심 차별화 포인트입니다!)

텍스트 전처리(Chunking): 수집한 문서를 LangChain의 RecursiveCharacterTextSplitter 등을 사용해 LLM이 소화하기 좋은 크기(Chunk)로 쪼갭니다.

[Phase 2: RAG 파이프라인 구축 (3~5일차)]

임베딩 & Vector DB 구축: 쪼갠 텍스트를 임베딩 모델(OpenAI text-embedding-ada-002 또는 무료인 HuggingFace 모델)을 이용해 벡터로 변환하고, 로컬에서 쓰기 편한 ChromaDB나 FAISS에 저장합니다.

Retriever 세팅: 사용자의 질문이 들어왔을 때, Vector DB에서 가장 관련성 높은 상품 문서(Top-K)를 검색해오는 로직을 짭니다.

[Phase 3: LLM 연동 및 프롬프트 엔지니어링 (6~7일차)]

프롬프트 설계: 검색된 문서(Context)와 가상 유저 데이터(Profile)를 바탕으로 답변을 생성하도록 프롬프트를 정교하게 깎습니다.

예: "당신은 하나은행의 전문 프라이빗 뱅커(PB)입니다. 다음 고객 정보와 검색된 금융 상품 정보를 바탕으로 최적의 상품을 추천하고 그 이유를 논리적으로 설명하세요."

LLM 연결: OpenAI API(GPT-3.5-turbo 또는 GPT-4o-mini)를 연결하여 답변을 생성합니다. 금융 도메인인 만큼 환각(Hallucination)을 최소화하도록 온도를 낮게(Temperature=0.1~0.3) 설정하는 것이 좋습니다.

[Phase 4: Streamlit UI 구현 및 마무​리 (8~10일차)]

UI 개발: Streamlit의 st.chat_message와 st.chat_input을 활용해 카카오톡 같은 챗봇 화면을 구성합니다.

사이드바 활용: 좌측 사이드바에 가상 고객의 프로필(나이, 소득, 투자 성향 등)을 조절할 수 있는 슬라이더나 드롭다운을 넣으면 포트폴리오 시연 영상에서 훨씬 전문적으로 보입니다.

GitHub 정리: Readme에 아키텍처 다이어그램, 문제 해결 과정(예: "검색 정확도를 높이기 위해 Chunk size를 어떻게 조절했다"), 시연 화면(GIF)을 깔끔하게 정리합니다.
