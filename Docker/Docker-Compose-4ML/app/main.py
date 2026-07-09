from fastapi import FastAPI
import httpx

app = FastAPI()

MODELLER = {
    "Logistic Regression": "http://logistic:8001",
    "Random Forest": "http://randomforest:8002",
    "KNN": "http://knn:8003",
    "SVM": "http://svm:8004"
}

@app.get("/")
def read_root():
    return {"mesaj": "Su Kalitesi Tahmin API'si çalışıyor!"}

@app.post("/tahmin")
async def tahmin(ph: float, hardness: float, solids: float, chloramines: float,
                 sulfate: float, conductivity: float, organic_carbon: float,
                 trihalomethanes: float, turbidity: float):
    
    params = {
        "ph": ph, "hardness": hardness, "solids": solids,
        "chloramines": chloramines, "sulfate": sulfate,
        "conductivity": conductivity, "organic_carbon": organic_carbon,
        "trihalomethanes": trihalomethanes, "turbidity": turbidity
    }
    
    sonuclar = {}
    async with httpx.AsyncClient() as client:
        for isim, url in MODELLER.items():
            response = await client.post(f"{url}/tahmin", params=params)
            sonuclar[isim] = response.json()
    
    return {"sonuclar": sonuclar}