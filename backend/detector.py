from collections import defaultdict
import os
import time
import logging
from database import SessionLocal, Alert

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "logs", "detector.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("threatvision.detector")


def analyze_logs():
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

    failed_attempts = defaultdict(int)
    alerts = []

    for line in lines:
        if "Failed password" in line:
            ip = line.split("from")[-1].strip()
            failed_attempts[ip] += 1

            if failed_attempts[ip] >= 3:
                alert = {
                    "type": "Brute Force Attack",
                    "ip": ip,
                    "severity": "HIGH",
                    "message": f"Multiple failed logins detected from {ip}"
                }
                alerts.append(alert)

    return alerts


def save_alerts(alerts):
    db = SessionLocal()
    for alert in alerts:
        alert_record = Alert(
            type=alert["type"],
            ip=alert["ip"],
            severity=alert["severity"],
            message=alert["message"]
        )
        db.add(alert_record)
    db.commit()
    db.close()


def monitor():
    logger.info("ThreatVision monitoring started")
    processed_lines = 0
    alerted_ips = set()

    while True:
        try:
            with open(LOG_FILE, "r") as file:
                lines = file.readlines()

            new_lines = lines[processed_lines:]

            if new_lines:
                failed_attempts = defaultdict(int)
                alerts = []

                for line in new_lines:
                    if "Failed password" in line:
                        ip = line.split("from")[-1].strip()
                        failed_attempts[ip] += 1

                        if failed_attempts[ip] >= 3 and ip not in alerted_ips:
                            alert = {
                                "type": "Brute Force Attack",
                                "ip": ip,
                                "severity": "HIGH",
                                "message": f"Multiple failed logins detected from {ip}"
                            }
                            alerts.append(alert)
                            alerted_ips.add(ip)
                            logger.warning(f"Brute force attack detected from {ip}")

                if alerts:
                    save_alerts(alerts)
                    logger.info(f"Saved {len(alerts)} new alerts to database")

                processed_lines = len(lines)

        except Exception as e:
            logger.error(f"Monitor error: {e}")

        time.sleep(5)


if __name__ == "__main__":
    monitor()