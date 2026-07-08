from fastapi import FastAPI
from database import SessionLocal, Alert

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ThreatVision API is running"}

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).all()
    db.close()
    return alerts