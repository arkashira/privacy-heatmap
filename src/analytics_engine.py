import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3

@dataclass
class VisitorEvent:
    id: int
    timestamp: datetime
    data: dict

class AnalyticsEngine:
    def __init__(self, db_path, retention_days):
        self.db_path = db_path
        self.retention_days = retention_days
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitor_events
            (id INTEGER PRIMARY KEY, timestamp TEXT, data TEXT)
        """)
        self.conn.commit()

    def store_event(self, event: VisitorEvent):
        self.cursor.execute("""
            INSERT INTO visitor_events (id, timestamp, data)
            VALUES (?, ?, ?)
        """, (event.id, event.timestamp.isoformat(), json.dumps(event.data)))
        self.conn.commit()

    def delete_old_data(self):
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        self.cursor.execute("""
            DELETE FROM visitor_events
            WHERE timestamp < ?
        """, (cutoff.isoformat(),))
        self.conn.commit()

    def close(self):
        self.conn.close()
