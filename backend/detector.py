from collections import defaultdict
import time

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "auth.log")

def analyze_logs():
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

    failed_attempts = defaultdict(int)
    alerts = []

    for line in lines:
        if "Failed password" in line:
            # extract IP (simple simulation)
            ip = line.split("from")[-1].strip()

            failed_attempts[ip] += 1

            # detection rule
            if failed_attempts[ip] >= 3:
                alert = {
                    "type": "Brute Force Attack",
                    "ip": ip,
                    "severity": "HIGH",
                    "message": f"Multiple failed logins detected from {ip}"
                }

                alerts.append(alert)

    return alerts


if __name__ == "__main__":
    alerts = analyze_logs()

    for alert in alerts:
        print("\n🚨 ALERT DETECTED")
        print(alert)