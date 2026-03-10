import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score

df = pd.read_csv("../data/data_processed.csv")

# 1. 데이터 로드 및 칼럼 선택 (앞서 한글화 전처리된 df 사용 가정)
selected_cols = ['연령', '직업', '결혼상태', '연간평균잔고', '주택담보대출여부', '개인신용대출여부', '정기예금가입여부']
df_selected = df[selected_cols].copy()

# 2. Target 값을 0과 1로 변환 ('예' -> 1, '아니오' -> 0)
df_selected['정기예금가입여부'] = df_selected['정기예금가입여부'].map({'예': 1, '아니오': 0})

# 3. 범주형 변수를 카테고리 타입으로 변환 (LightGBM, CatBoost를 위해)
cat_features = ['직업', '결혼상태', '주택담보대출여부', '개인신용대출여부']
for col in cat_features:
    df_selected[col] = df_selected[col].astype('category')

# 4. Train / Test Split
X = df_selected.drop('정기예금가입여부', axis=1)
y = df_selected['정기예금가입여부']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 모델 정의
models = {
    # XGBoost는 범주형 변수를 위해 enable_categorical=True 설정 필요 (최신 버전 기준)
    "XGBoost": XGBClassifier(enable_categorical=True, random_state=42),
    
    # LightGBM은 category 타입을 자동 인식
    "LightGBM": LGBMClassifier(random_state=42),
    
    # CatBoost는 범주형 피처 리스트를 직접 전달
    "CatBoost": CatBoostClassifier(cat_features=list(X_train.columns.get_indexer(cat_features)), verbose=0, random_state=42)
}

# 6. 모델 비교 학습 및 평가
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(f"=== {name} ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}\n")