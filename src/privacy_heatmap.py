import json
from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    event_type: str
    event_data: dict

class PrivacyHeatmap:
    def __init__(self):
        self.events = []

    def capture_event(self, event_type: str, event_data: dict):
        event = Event(event_type, event_data)
        self.events.append(event)

    def post_events(self, endpoint: str):
        event_data = [event.__dict__ for event in self.events]
        return json.dumps(event_data)

    def persist_events(self, db_connection):
        for event in self.events:
            db_connection.execute("INSERT INTO wp_privacy_heatmap_events (event_type, event_data) VALUES (%s, %s)", (event.event_type, json.dumps(event.event_data)))
