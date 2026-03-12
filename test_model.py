import pandas as pd
from catboost import CatBoostClassifier

# ==========================================
# 1. 저장된 모델 불러오기
# ==========================================
print("🔄 'catboost_bank_model.cbm' 모델을 불러오는 중...")
model = CatBoostClassifier()
model.load_model("./model/catboost_bank_model.cbm")
print("✅ 모델 로드 완료!\n")

# ==========================================
# 2. 테스트용 가상 고객 데이터 생성
# (실제 챗봇에서는 은행 DB나 사용자 입력에서 가져올 데이터입니다)
# ==========================================
# 모델 학습에 사용했던 6개 칼럼 순서와 이름을 정확히 맞춰야 합니다.
test_customers = [
    {
        '연령': 32,
        '직업': '사무직',
        '결혼상태': '미혼',
        '연간평균잔고': 3500,
        '주택담보대출여부': '아니오',
        '개인신용대출여부': '아니오'
    },
    {
        '연령': 45,
        '직업': '생산직',
        '결혼상태': '기혼',
        '연간평균잔고': 150,
        '주택담보대출여부': '예',
        '개인신용대출여부': '예'
    },
    {
        '연령': 65,
        '직업': '은퇴자',
        '결혼상태': '기혼',
        '연간평균잔고': 8000,
        '주택담보대출여부': '아니오',
        '개인신용대출여부': '아니오'

    },
    {
         '연령': 25,
        '직업': '은퇴자',
        '결혼상태': '기혼',
        '연간평균잔고': 100,
        '주택담보대출여부': '아니오',
        '개인신용대출여부': '아니오'

    }
]

# 딕셔너리 리스트를 Pandas DataFrame으로 변환
test_df = pd.DataFrame(test_customers)

# ==========================================
# 3. 모델 예측 수행 및 결과 출력
# ==========================================
print("=" * 50)
print("📊 [가상 고객 타겟팅 예측 테스트]")
print("=" * 50)

# predict: 0 (가입 안함) 또는 1 (가입 함)
predictions = model.predict(test_df)
# predict_proba: [가입 안할 확률, 가입 할 확률]
probabilities = model.predict_proba(test_df)

for i in range(len(test_df)):
    print(f"👤 [고객 {i+1} 프로필]")
    print(test_df.iloc[i].to_dict())
    
    pred_class = predictions[i]
    prob_yes = probabilities[i][1] * 100  # 1(가입)에 해당하는 확률을 백분율로 변환
    
    # 예측 결과에 따른 시각적 텍스트 처리
    if pred_class == 1:
        result_text = "🟢 가입 가능성 높음 (우선 타겟 고객)"
    else:
        result_text = "🔴 가입 가능성 낮음 (일반 고객)"
        
    print(f"\n👉 AI 예측 클래스: {result_text}")
    print(f"👉 예금 가입(여유 자금 예치) 성향 점수: {prob_yes:.2f}%")
    print("-" * 50)