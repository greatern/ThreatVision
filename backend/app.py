from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import SessionLocal, Alert

app = FastAPI()

# --- CORS ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---

class AlertResponse(BaseModel):
    id: int
    type: str
    ip: str
    severity: str
    message: str

    class Config:
        from_attributes = True


class SummaryResponse(BaseModel):
    total: int
    high: int
    medium: int
    low: int


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "ThreatVision API is running"}


@app.get("/alerts", response_model=List[AlertResponse])
def get_alerts():
    db = SessionLocal()
    try:
        alerts = db.query(Alert).all()
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts")
    finally:
        db.close()


@app.get("/alerts/summary", response_model=SummaryResponse)
def get_summary():
    db = SessionLocal()
    try:
        total = db.query(Alert).count()
        high = db.query(Alert).filter(Alert.severity == "HIGH").count()
        medium = db.query(Alert).filter(Alert.severity == "MEDIUM").count()
        low = db.query(Alert).filter(Alert.severity == "LOW").count()
        return {"total": total, "high": high, "medium": medium, "low": low}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve summary")
    finally:
        db.close()


@app.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int):
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve alert")
    finally:
        db.close()


@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int):
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        db.delete(alert)
        db.commit()
        return {"message": f"Alert {alert_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete alert")
    finally:
        db.close()