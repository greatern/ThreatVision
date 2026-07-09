from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import SessionLocal, Alert
import threading
import logging
import os
import time
from detector import monitor

# --- Logging Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "api.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("threatvision.api")

app = FastAPI()

START_TIME = time.time()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Start background monitor ---
logger.info("Starting background monitor thread...")
monitor_thread = threading.Thread(target=monitor, daemon=True)
monitor_thread.start()
logger.info("Monitor thread started successfully")

# --- Pydantic Schemas ---
class AlertResponse(BaseModel):
    id: int
    type: str
    ip: str
    severity: str
    message: str
    timestamp: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SummaryResponse(BaseModel):
    total: int
    high: int
    medium: int
    low: int


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    database: str
    monitor: str


# --- Endpoints ---
@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "ThreatVision API is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    uptime = round(time.time() - START_TIME, 2)
    db_status = "ok"
    try:
        db = SessionLocal()
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = "error"
        logger.error(f"Health check database error: {e}")
    monitor_status = "running" if monitor_thread.is_alive() else "stopped"
    logger.info(f"Health check - uptime: {uptime}s, db: {db_status}, monitor: {monitor_status}")
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "uptime_seconds": uptime,
        "database": db_status,
        "monitor": monitor_status
    }


@app.get("/alerts", response_model=List[AlertResponse])
def get_alerts():
    db = SessionLocal()
    try:
        alerts = db.query(Alert).all()
        logger.info(f"Retrieved {len(alerts)} alerts")
        return alerts
    except Exception as e:
        logger.error(f"Failed to retrieve alerts: {e}")
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
        logger.info(f"Summary - total: {total}, high: {high}, medium: {medium}, low: {low}")
        return {"total": total, "high": high, "medium": medium, "low": low}
    except Exception as e:
        logger.error(f"Failed to retrieve summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve summary")
    finally:
        db.close()


@app.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int):
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            logger.warning(f"Alert {alert_id} not found")
            raise HTTPException(status_code=404, detail="Alert not found")
        logger.info(f"Retrieved alert {alert_id}")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve alert")
    finally:
        db.close()


@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int):
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            logger.warning(f"Attempted to delete non-existent alert {alert_id}")
            raise HTTPException(status_code=404, detail="Alert not found")
        db.delete(alert)
        db.commit()
        logger.info(f"Deleted alert {alert_id}")
        return {"message": f"Alert {alert_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete alert")
    finally:
        db.close()