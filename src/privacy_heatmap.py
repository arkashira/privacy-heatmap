import datetime
import json
from dataclasses import dataclass
from typing import List

@dataclass
class LogEntry:
    timestamp: datetime.datetime
    records_purged: int

class PrivacyHeatmap:
    def __init__(self, retention_days: int = 90):
        self.retention_days = retention_days
        self.records = []
        self.log = []

    def add_record(self, record: dict):
        self.records.append(record)

    def purge_records(self):
        cutoff = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
        purged_records = [record for record in self.records if record['timestamp'] < cutoff]
        self.records = [record for record in self.records if record['timestamp'] >= cutoff]
        if purged_records:
            self.log.append(LogEntry(datetime.datetime.now(), len(purged_records)))
        return len(purged_records)

    def get_log(self):
        return self.log

    def set_retention_days(self, days: int):
        self.retention_days = days
