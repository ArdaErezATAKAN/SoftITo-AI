from fastapi import FastAPI
import httpx
import os

app = FastAPI(title="İnme Riski Tahmin API Gateway")

GRADIENT_URL = os.getenv("GRADIENT_URL", "http://ml-gradient:5001")
DECISION_URL = os.getenv("DECISION_URL", "http://ml-decision:5002")
NAIVEBAYES_URL = os.getenv("NAIVEBAYES_URL", "http://ml-naivebayes:5003")
NEURAL_URL = os.getenv("NEURAL_URL", "http://ml-neural:5004")

MODELLER = {
    "Gradient Boosting": GRADIENT_URL,
    "Decision Tree": DECISION_URL,
    "Naive Bayes": NAIVEBAYES_URL,
    "Neural Network": NEURAL_URL
}

@app.get("/")
def read_root():
    return {"mesaj": "İnme Riski Tahmin API Gateway çalışıyor!"}

@app.post("/tahmin")
async def tahmin(
    gender: str, age: float, hypertension: int, heart_disease: int,
    ever_married: str, work_type: str, residence_type: str,
    avg_glucose_level: float, bmi: float, smoking_status: str
):
    params = {
        "gender": gender, "age": age, "hypertension": hypertension,
        "heart_disease": heart_disease, "ever_married": ever_married,
        "work_type": work_type, "residence_type": residence_type,
        "avg_glucose_level": avg_glucose_level, "bmi": bmi,
        "smoking_status": smoking_status
    }

    sonuclar = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        for isim, url in MODELLER.items():
            try:
                response = await client.post(f"{url}/tahmin", params=params)
                sonuclar[isim] = response.json()
            except Exception as e:
                sonuclar[isim] = {"hata": str(e)}

    return {"sonuclar": sonuclar}