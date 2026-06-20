import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse

@dataclass
class AuditLog:
    user_id: int
    timestamp: str
    action: str

class PrivacyHeatmap:
    def __init__(self, log_retention=180):
        self.log_retention = log_retention
        self.audit_log = []

    def log_access(self, user_id, action):
        self.audit_log.append(AuditLog(user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action))
        self._prune_log()

    def _prune_log(self):
        cutoff = datetime.now() - timedelta(days=self.log_retention)
        self.audit_log = [log for log in self.audit_log if datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S") > cutoff]

    def export_log(self):
        return json.dumps([{"user_id": log.user_id, "timestamp": log.timestamp, "action": log.action} for log in self.audit_log])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-retention", type=int, default=180)
    args = parser.parse_args()
    heatmap = PrivacyHeatmap(args.log_retention)
    heatmap.log_access(1, "read")
    heatmap.log_access(2, "write")
    print(heatmap.export_log())

if __name__ == "__main__":
    main()
