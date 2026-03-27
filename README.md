#  FinRAG Advisor: Financial AI Agent System
> **익명 사용자 맞춤 금융상품 추천 챗봇** 고객의 입력 데이터를 기반으로 성향을 분석하고, RAG(검색 증강 생성) 기술을 활용하여 하나은행의 실제 금융 상품 약관에 기반한 맞춤형 상품을 추천 및 상담해 주는 AI 뱅커 서비스입니다.
> 제작 기간: 2026.03.04. ~ 2026.03.14.

## 1.Project Overview (프로젝트 개요)
이 프로젝트는 API 호출형 챗봇을 넘어, **실제 금융권 실무 환경의 데이터 제약과 복잡성을 반영한 하이브리드 추천 파이프라인**입니다. 
고객의 정형 데이터(행동 로그, 자산 정보)를 분석하는 ML 예측 모델과, 비정형 데이터(복잡한 금융 약관 PDF)를 분석하는 LLM 기반 Agentic RAG를 결합하여, 환각 현상(Hallucination)을 제어하고 고도의 개인화된 금융 컨설팅 경험을 제공합니다.

### 기획 및 개발 목표
- **Hybrid AI 도입:** 규칙 기반이나 단순 LLM 챗봇을 넘어, **전통적 ML(가입 확률 예측)과 GenAI(맞춤형 설명 생성)의 결합** 시너지 창출
- **빅데이터 파이프라인 시뮬레이션:** 대용량 가상 고객 데이터 전처리 및 피처 엔지니어링 파이프라인(PySpark) 구축
- **의도 기반 동적 라우팅(Agentic RAG):** LangGraph를 활용해 사용자의 질문 의도에 따라 정형 DB(RDB)와 비정형 DB(Vector DB)를 스스로 탐색하는 멀티 에이전트 설계

---
## 주요 기능
- **머신러닝 기반 고객 맞춤 진단**: 사이드바를 통해 입력받은 사용자 정보(연령, 자산 등)를 바탕으로 ML 모델(CatBoost)이 고객의 예치 성향 등을 예측합니다.
- **문맥 인지형 AI 상담 (RAG 기반)**: LangChain을 활용해 사용자의 질문 문맥을 고도화하고, 문서화된 실제 금융 상품 정보를 검색하여 정확한 답변을 제공합니다.
- **스마트 질의 재작성 (Query Rewriting)**: "저 상품", "이거"와 같은 대명사를 포함한 연속적인 질문을 AI가 독립적인 문장으로 재작성하여, 대화의 맥락을 놓치지 않고 정확한 타겟 상품 정보를 검색합니다.

---

## 2. Tech Stack (기술 스택)

### Data Pipeline & ML (데이터 분석 및 예측 모델링)
- **Data Processing:** Python, Pandas, RecursiveCharacterTextSplitter, PyPDFDirectoryLoader
- **Machine Learning:** **CatBoost** (사용자 성향 및 금융 데이터 예측 모델)

### Generative AI & RAG (생성형 AI 및 검색 증강 생성)
- **Framework:** **LangChain, LangGraph** (Multi-Agent Routing)
- **LLM / Embedding:** Gemini 2.5 Flash, HuggingFace (`jhgan/ko-sroberta-multitask`)
- **Vector Database:** **ChromaDB**

### Frontend & Ops
- **UI/UX:** Streamlit

### DevOps / Infra
- Docker, Docker Compose
---
## 3. RAG 구성 (Retrieval-Augmented Generation)
- **데이터 소스**: 하나은행 주요 금융 상품 설명서 및 약관 PDF (예: 1년 연동형 정기예금.pdf, 3,6,9 정기예금.pdf 등)
- **임베딩 모델**: jhgan/ko-sroberta-multitask (한국어 문장 임베딩에 최적화된 모델 적용)
- **검색 방식**: 코사인 유사도 기반 검색 (Similarity Search) 및 타겟 상품명 기반 필터링 (Exact Product Filtering)

### 파이프라인 흐름
-**사용자 질문 입력**: 사용자가 채팅창에 질문 입력
-**질문 고도화**: LLM이 이전 대화 기록을 참고하여 질문을 완벽한 독립 문장으로 재작성 및 타겟 상품명 추출
-**벡터 검색 (Retriever)**: 재작성된 질문을 임베딩하여 Chroma DB에서 가장 유사한 약관 청크(Chunk) 검색 (k=4)
-**컨텍스트 융합**: 검색된 약관 원문 + ML이 분석한 고객 프로필 정보 결합

LLM 응답 생성: Gemini 모델이 환각(Hallucination) 없이 정확한 맞춤형 답변 생성 및 반환
---
## 4. System Architecture (시스템 구조)
*(여기에 데이터 파이프라인과 RAG 아키텍처가 결합된 다이어그램 이미지를 삽입하세요)*

1. **[Data Pipeline]** `PySpark`를 활용한 대용량 고객 거래/로그 데이터 전처리 및 ML 피처(Feature) 적재
2. **[ML Engine]** `XGBoost` 분류 모델을 통해 현재 고객 프로필(나이, 소득, 자산, 성향) 대비 가입 확률이 가장 높은 Top-N 금융 상품 1차 추천
3. **[Vector Search]** ML이 추천한 타겟 상품(Target Product)의 약관(PDF)만 `ChromaDB`에서 정밀 필터링(Metadata Filtering)하여 추출
4. **[Agentic LLM]** `LangGraph` 에이전트가 고객 프로필 데이터와 추출된 약관 조각(Chunk)을 종합하여 논리적이고 개인화된 설명(Reasoning) 생성

---

## 4. 구현 상세 및 주요 특징

### 하이브리드 금융 상품 추천 방식
- 사용자 질문에만 의존하지 않고, ML 모델이 측정한 고객의 '예치성향점수'와 '연령'을 프롬프트에 동적으로 주입합니다. 고객의 현재 상황(목돈 굴리기, 소액 짠테크, 시니어 노후 자금 등)에 맞춰 타겟화된 검색 쿼리를 스스로 최적화하여 맞춤형 상품을 안내합니다.

### 정확도 향상 전략 (Prompt Engineering & Query Rewriting)
- LLM에 전적으로 의존할 때 발생하는 비논리적 추천과 환각 현상을 방지.
- 사용자가 이전 답변에 이어서 "그럼 그 상품 금리는 얼마야?"라고 물었을 때, AI가 이를 "3,6,9 정기예금 상품의 금리는 얼마인가요?"로 자동 변환하여 검색 정확도를 극대화합니다.

### LangGraph를 활용한 Agentic RAG 시스템
- **Multi-Turn Context 관리:** 고객의 이전 대화를 기억하고 독립적인 검색 쿼리로 재작성(Query Rewriting).
- **노이즈 클렌징 (정규식):** PDF 파싱 과정에서 발생하는 헤더/푸터/웹 네비게이션 노이즈를 정규표현식으로 완벽히 제거하여 임베딩 품질 상향.

### Hallucination(환각) 방지 체계
-답변 생성 시 반드시 Chroma DB에서 가져온 출처(Source)와 페이지(Page)가 명시된 약관 데이터를 기반으로만 응답하도록 시스템 프롬프트를 구성하였습니다. 날짜, URL 등 불필요한 노이즈 텍스트는 전처리 단계에서 정규식으로 안전하게 제거하여 LLM의 문맥 이해도를 높였습니다.

---

## 5. Directory Structure (디렉토리 구조)
```text
llm-banker-rag-chatbot/
│
├── Dockerfile                 # 도커 이미지 빌드 파일
├── docker-compose.yml         # 도커 컨테이너 오케스트레이션
├── app.py                     # Streamlit 앱 메인 엔트리 포인트
├── main.py                    # 로컬 테스트용 메인 스크립트
├── rag_pipeline.py            # PDF 데이터 로드, 전처리 및 Vector DB 구축
├── requirements.txt           # 의존성 패키지 목록
│
├── core/                      # 핵심 비즈니스 로직
│   ├── llm_engine.py          # Query Rewriting 및 LLM 체인 (Gemini) 구성
│   ├── prompts.py             # 시스템 및 챗봇 프롬프트 템플릿
│   └── retriever.py           # Chroma DB 검색 및 타겟 상품 필터링 로직
│
├── data/                      # RAG 대상 데이터 (하나은행 약관 PDF, CSV 데이터)
│
├── data_processing/           # 데이터 분석 및 ML 모델 학습 코드
│   ├── processing.ipynb       # 전처리 주피터 노트북
│   └── train_catboost.py      # CatBoost 모델 학습 스크립트
│
├── model/                     # 학습된 머신러닝 모델 가중치 (CatBoost .cbm)
│
├── ui/                        # Streamlit 프론트엔드 UI 컴포넌트
│   ├── chat_page.py           # 채팅 인터페이스 렌더링
│   └── sidebar.py             # 사용자 프로필 입력 사이드바
│
├── utils/                     # 공통 유틸리티 
│   └── logger.py              # 시스템 로깅 설정
│
├── logs/                      # 사용자 대화 로그 폴더
└── db/                        # 생성된 Chroma Vector DB 디렉토리 (자동 생성됨)

```
ㅡㅡㅡ

## 설치 및 실행 방법

### 이 프로젝트는 로컬 환경에 직접 설치하거나, Docker를 사용하여 간편하게 실행할 수 있습니다.


### 공통: 저장소 클론 및 환경 변수 설정
1. 저장소 클론
git clone https://github.com/skidroww/llm-banker-rag-chatbot.git
cd llm-banker-rag-chatbot

2. 환경 변수 파일 생성 (.env)
echo 'GOOGLE_API_KEY="본인의_API_키를_입력하세요"' > .env


### 옵션 A: Docker를 이용한 실행 (권장)
로컬 환경을 오염시키지 않고 가장 빠르게 실행하는 방법입니다. Docker와 Docker Compose가 설치되어 있어야 합니다.
컨테이너 빌드 및 백그라운드 실행
docker-compose up -d --build

실행 확인 및 로그 보기
docker-compose logs -f

실행이 완료되면 브라우저에서 http://localhost:8501로 접속하여 챗봇을 사용할 수 있습니다.

### B: 로컬 환경(Python)에서 직접 실행
Python 3.9 이상의 환경을 권장합니다. 가상환경(venv)을 사용하는 것을 추천합니다.
1. 패키지 설치
pip install -r requirements.txt

2. Vector DB 빌드 (초기 1회 필수)
PDF 데이터로부터 Chroma DB를 생성합니다.
python rag_pipeline.py

3. 애플리케이션 실행
streamlit run app.py

---

+---------------------------------------------------------------------------------+
|                    [ Data Pipeline & RAG Architecture ]                         |
+---------------------------------------------------------------------------------+

===================================================================================
[ 1. Data Pipeline (Offline / Async) ] - 데이터 수집 및 벡터화
===================================================================================

  📄 Raw Documents 
  (하나은행 상품 PDF, CSV)
         │
         ▼
  ✂️ Data Processor 
  (Document Loader & RecursiveCharacterTextSplitter)
         │
         ▼
  🧠 Embedding Model 
  (jhgan/ko-sroberta-multitask)
         │
         ▼
  🗄️ Vector Database (Chroma DB)  <====================================+
  (Stores Document Embeddings & Metadata)                              ‖
                                                                       ‖
                                                                       ‖
=======================================================================‖===========
[ 2. RAG Pipeline (Online / Real-time) ] - 실시간 질의응답 및 추천     ‖
=======================================================================‖===========
                                                                       ‖
  👤 User Input (채팅창 입력) ──────────────────────────┐              ‖
         │                                              │              ‖
         ▼                                              ▼              ‖
  📊 ML Model (CatBoost)                      🧠 Query Rewriter (LLM)  ‖
  (고객 예치 성향 및 프로필 예측)             (대명사 해석 및 질문 고도화) 
         │                                              │              ‖
         │                                              ▼              ‖
         │                                    🧠 Embedding Model       ‖
         │                                    (User Query Vectorized)  ‖
         │                                              │              ‖
         │                                              ▼              ‖
         │                                    🔍 Similarity Search  ===+ 
         │                                    (Top-K Context Retrieval)
         │                                              │
         └──────────────────────+                       │ [Retrieved Contexts]
                                │                       │
                                ▼                       ▼
                              📝 Prompt Builder
                              (System Instructions + Context + ML Profile Data)
                                            │
                                            ▼
                              🤖 LLM Engine (Gemini 3.1 Pro)
                              (Context-Aware Generation)
                                            │
                                            ▼
                              💬 Final Response (사용자 맞춤형 답변 제공)
