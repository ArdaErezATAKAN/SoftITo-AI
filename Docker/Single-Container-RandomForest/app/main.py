from fastapi import FastAPI
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = FastAPI()

df = pd.read_csv("diabetes.csv")
X = df.drop("Outcome", axis=1)
y = df["Outcome"]
model = RandomForestClassifier()
model.fit(X, y)

@app.get("/")
def read_root():
    return {"mesaj": "Diyabet tahmin API'si çalışıyor!"}

@app.post("/tahmin")
def tahmin(pregnancies: int, glucose: int, blood_pressure: int,
           skin_thickness: int, insulin: int, bmi: float,
           diabetes_pedigree: float, age: int):
    veri = np.array([[pregnancies, glucose, blood_pressure,
                      skin_thickness, insulin, bmi,
                      diabetes_pedigree, age]])
    sonuc = model.predict(veri)[0]
    return {"diyabet_var_mi": bool(sonuc)}