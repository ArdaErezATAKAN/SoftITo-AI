from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

df = pd.read_csv("/data/healthcare-dataset-stroke-data.csv")
df = df.drop("id", axis=1)

le = LabelEncoder()
for col in ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]:
    df[col] = le.fit_transform(df[col].astype(str))

X = df.drop("stroke", axis=1)
y = df["stroke"]

imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingClassifier()
model.fit(X_train, y_train)
dogruluk = accuracy_score(y_test, model.predict(X_test))

@app.post("/tahmin")
def tahmin(gender: str, age: float, hypertension: int, heart_disease: int,
           ever_married: str, work_type: str, residence_type: str,
           avg_glucose_level: float, bmi: float, smoking_status: str):
    
    veri = pd.DataFrame([[gender, age, hypertension, heart_disease,
                          ever_married, work_type, residence_type,
                          avg_glucose_level, bmi, smoking_status]],
                        columns=["gender", "age", "hypertension", "heart_disease",
                                 "ever_married", "work_type", "Residence_type",
                                 "avg_glucose_level", "bmi", "smoking_status"])
    
    for col in ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]:
        veri[col] = le.fit_transform(veri[col].astype(str))
    
    veri = imputer.transform(veri)
    sonuc = model.predict(veri)[0]
    return {"inme_riski": bool(sonuc), "model_dogrulugu": round(dogruluk * 100, 2)}