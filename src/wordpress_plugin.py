import json
from dataclasses import dataclass
from typing import List

@dataclass
class UserInteraction:
    mouse_movements: List[tuple]
    clicks: List[tuple]
    scrolls: List[tuple]

class WordPressPlugin:
    def __init__(self):
        self.interactions = []

    def track_mouse_movements(self, movements: List[tuple]):
        self.interactions.append(UserInteraction(mouse_movements=movements, clicks=[], scrolls=[]))

    def track_clicks(self, clicks: List[tuple]):
        self.interactions.append(UserInteraction(mouse_movements=[], clicks=clicks, scrolls=[]))

    def track_scrolls(self, scrolls: List[tuple]):
        self.interactions.append(UserInteraction(mouse_movements=[], clicks=[], scrolls=scrolls))

    def anonymize_ip_device_data(self, ip: str, device: str):
        return "anonymized_ip", "anonymized_device"

    def store_raw_events(self, events: List[UserInteraction]):
        # In-memory stand-in for PostgreSQL
        self.events = events

    def send_anonymized_session_data(self, events: List[UserInteraction]):
        anonymized_events = []
        for event in events:
            anonymized_event = {
                "mouse_movements": event.mouse_movements,
                "clicks": event.clicks,
                "scrolls": event.scrolls,
                "ip": self.anonymize_ip_device_data("192.168.1.1", "Desktop")[0],
                "device": self.anonymize_ip_device_data("192.168.1.1", "Desktop")[1]
            }
            anonymized_events.append(anonymized_event)
        return anonymized_events
