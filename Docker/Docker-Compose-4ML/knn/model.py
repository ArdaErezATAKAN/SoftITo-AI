from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

app = FastAPI()

df = pd.read_csv("water_potability.csv")
X = df.drop("Potability", axis=1)
y = df["Potability"]
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = KNeighborsClassifier()
model.fit(X_train, y_train)
dogruluk = accuracy_score(y_test, model.predict(X_test))

@app.post("/tahmin")
def tahmin(ph: float, hardness: float, solids: float, chloramines: float,
           sulfate: float, conductivity: float, organic_carbon: float,
           trihalomethanes: float, turbidity: float):
    veri = np.array([[ph, hardness, solids, chloramines,
                      sulfate, conductivity, organic_carbon,
                      trihalomethanes, turbidity]])
    sonuc = model.predict(veri)[0]
    return {"iciliebilir_mi": bool(sonuc), "model_dogrulugu": round(dogruluk * 100, 2)}