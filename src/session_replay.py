import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import time

@dataclass
class SessionEvent:
    timestamp: datetime
    event_type: str
    data: dict

class SessionReplay:
    def __init__(self, session_events):
        self.session_events = session_events
        self.current_time = 0
        self.playing = False

    def load(self):
        start_time = time.time()
        # Simulate loading session events
        time.sleep(0.1)
        end_time = time.time()
        if end_time - start_time > 3:
            raise Exception("Session replay took too long to load")

    def play(self):
        self.playing = True
        for event in self.session_events:
            while self.playing and self.current_time < (event.timestamp - self.session_events[0].timestamp).total_seconds():
                time.sleep(0.01)
                self.current_time += 0.01
            if not self.playing:
                break
            yield event

    def pause(self):
        self.playing = False

    def resume(self):
        self.playing = True

    def scrub(self, timestamp):
        self.current_time = timestamp
        self.playing = False
