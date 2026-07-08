from collections import defaultdict
import os
from database import SessionLocal, Alert

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")

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


if __name__ == "__main__":
    alerts = analyze_logs()
    save_alerts(alerts)

    for alert in alerts:
        print("\n🚨 ALERT DETECTED")
        print(alert)