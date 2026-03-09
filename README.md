# 🏦 FinRAG Advisor: Enterprise Financial AI Agent System
> **생성형 AI와 머신러닝(ML), 빅데이터 파이프라인을 융합한 엔터프라이즈급 맞춤형 금융 상품 추천 시스템**
> 제작 기간: 2026.03.04. ~ 진행 중

## 1. Project Overview (프로젝트 개요)
본 프로젝트는 단순한 API 호출형 챗봇을 넘어, **실제 금융권 실무 환경의 데이터 제약과 복잡성을 반영한 하이브리드 추천 파이프라인**입니다. 
고객의 정형 데이터(행동 로그, 자산 정보)를 분석하는 ML 예측 모델과, 비정형 데이터(복잡한 금융 약관 PDF)를 분석하는 LLM 기반 Agentic RAG를 결합하여, 환각 현상(Hallucination)을 제어하고 고도의 개인화된 금융 컨설팅 경험을 제공합니다.

### 🎯 기획 및 개발 목표
- **Hybrid AI 도입:** 규칙 기반이나 단순 LLM 의존을 탈피하여, **전통적 ML(가입 확률 예측)과 GenAI(맞춤형 설명 생성)의 결합** 시너지 창출
- **빅데이터 파이프라인 시뮬레이션:** 대용량 가상 고객 데이터 전처리 및 피처 엔지니어링 파이프라인(PySpark) 구축
- **의도 기반 동적 라우팅(Agentic RAG):** LangGraph를 활용해 사용자의 질문 의도에 따라 정형 DB(RDB)와 비정형 DB(Vector DB)를 스스로 탐색하는 멀티 에이전트 설계

---

## 2. Tech Stack (기술 스택)

### 📊 Data Pipeline & ML (데이터 분석 및 예측 모델링)
- **Data Processing:** Python, **PySpark**, Pandas
- **Machine Learning:** **XGBoost**, LightGBM, scikit-learn

### 🧠 Generative AI & RAG (생성형 AI 및 검색 증강 생성)
- **Framework:** **LangChain, LangGraph** (Multi-Agent Routing)
- **LLM / Embedding:** Gemini 2.5 Flash, HuggingFace (`jhgan/ko-sroberta-multitask`)
- **Vector Database:** **ChromaDB**

### 💻 Frontend & Ops
- **UI/UX:** Streamlit
- **Environment:** dotenv, Git

---

## 3. System Architecture (시스템 구조)
*(여기에 데이터 파이프라인과 RAG 아키텍처가 결합된 다이어그램 이미지를 삽입하세요)*

1. **[Data Pipeline]** `PySpark`를 활용한 대용량 고객 거래/로그 데이터 전처리 및 ML 피처(Feature) 적재
2. **[ML Engine]** `XGBoost` 분류 모델을 통해 현재 고객 프로필(나이, 소득, 자산, 성향) 대비 가입 확률이 가장 높은 Top-N 금융 상품 1차 추천
3. **[Vector Search]** ML이 추천한 타겟 상품(Target Product)의 약관(PDF)만 `ChromaDB`에서 정밀 필터링(Metadata Filtering)하여 추출
4. **[Agentic LLM]** `LangGraph` 에이전트가 고객 프로필 데이터와 추출된 약관 조각(Chunk)을 종합하여 논리적이고 개인화된 설명(Reasoning) 생성

---

## 4. Key Features (핵심 기능 및 구현 상세)

### ✨ 4.1. PySpark 기반 대용량 데이터 전처리 및 피처 엔지니어링
- 가상의 대규모 금융 거래/로그 데이터를 생성하고, 결측치 처리 및 파생 변수 생성을 분산 처리 환경(Spark)에서 수행하는 파이프라인 시뮬레이션 구축.

### ✨ 4.2. XGBoost + LLM 하이브리드 추천 엔진
- LLM에 전적으로 의존할 때 발생하는 비논리적 추천과 환각 현상을 방지.
- 실제 데이터 기반의 머신러닝(XGBoost)이 상품을 1차 필터링하고, LLM은 해당 결과를 고객이 이해하기 쉬운 언어로 풀어내는 '설명 가능한 AI(XAI)' 역할 수행.

### ✨ 4.3. LangGraph를 활용한 Agentic RAG 시스템
- **Multi-Turn Context 관리:** 고객의 이전 대화를 기억하고 독립적인 검색 쿼리로 재작성(Query Rewriting).
- **Tool Routing:** 고객 질문이 자산 현황 조회를 요하는지, 상품 약관 검색을 요하는지 Agent가 스스로 판단하여 적합한 데이터베이스(RDB vs VectorDB) 호출.
- **노이즈 클렌징 (정규식):** PDF 파싱 과정에서 발생하는 헤더/푸터/웹 네비게이션 노이즈를 정규표현식으로 완벽히 제거하여 임베딩 품질 극대화.

---

## 5. Directory Structure (디렉토리 구조)
```text
llm-banker-rag-chatbot/
├── data/                    # 금융 상품 약관 PDF 파일 모음
├── db/                      # ChromaDB Vector Store 저장소
├── core/
│   ├── llm_engine.py        # LangGraph 에이전트 및 LLM 추론 코어
│   ├── prompts.py           # 페르소나 및 RAG 프롬프트 템플릿
│   └── retriever.py         # 메타데이터 필터링 및 VectorDB 검색 로직
├── ml_pipeline/             # [NEW] 머신러닝 파이프라인
│   ├── spark_data_prep.py   # PySpark 기반 대규모 데이터 전처리
│   └── train_xgb_model.py   # 상품 가입 확률 예측 모델 학습
├── ui/
│   ├── chat_page.py         # Streamlit 챗봇 UI
│   └── sidebar.py           # 고객 프로필 및 자산 입력 폼
├── rag_pipeline.py          # PDF 파싱, 정규식 전처리, Chunking 및 임베딩 스크립트
├── app.py                   # 애플리케이션 엔트리 포인트
└── README.md