import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report 


df = pd.read_csv(r"C:\Users\playdata2\Desktop\llm-banker-rag-chatbot\data\data_processed.csv")
                 



selected_cols = ['연령', '직업', '결혼상태', '연간평균잔고', '주택담보대출여부', '개인신용대출여부', '정기예금가입여부']
df_selected = df[selected_cols].copy()
df_selected['정기예금가입여부'] = df_selected['정기예금가입여부'].map({'예': 1, '아니오': 0})

cat_features = ['직업', '결혼상태', '주택담보대출여부', '개인신용대출여부']

X = df_selected.drop('정기예금가입여부', axis=1)
y = df_selected['정기예금가입여부']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    cat_features=cat_features,
    random_state=42,
    verbose=50
)



print("모델 학습을 시작합니다...")
model.fit(X_train, y_train)
print(" 학습 완료\n")


print("="*40)
print("[모델 성능 평가 결과]")
print("="*40)

# 예측 수행 (테스트 데이터 사용)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# 1. 기본 평가 지표 출력
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
print(f" Accuracy (정확도): {acc:.4f}")
print(f" ROC-AUC 스코어  : {auc:.4f}\n")

# 2. 상세 평가 리포트 출력 (Precision, Recall, F1-Score)
print("상세 분류 리포트 (Classification Report):")
print(classification_report(y_test, y_pred, target_names=['가입 안함(0)', '가입 함(1)']))
print("="*40)
# ==========================================




model.save_model("catboost_bank_model.cbm")
print("\n 모델이 'catboost_bank_model.cbm' 파일로 성공적으로 저장되었습니다.")