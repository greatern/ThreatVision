from fastapi import FastAPI

app = FastAPI()

alerts = []

@app.get("/")
def home():
    return {"message": "ThreatVision API Running"}

@app.get("/alerts")
def get_alerts():
    return alerts