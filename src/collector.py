import json
from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    type: str
    data: dict

class Collector:
    def __init__(self):
        self.events = []

    def collect(self, event: Event):
        self.events.append(event)

    def store(self, db: dict):
        for event in self.events:
            db[event.type] = db.get(event.type, []) + [event.data]

    def get_script(self) -> str:
        script = """
        function collectEvent(event) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/collect', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(event));
        }

        document.addEventListener('click', function(event) {
            collectEvent({ type: 'click', data: { x: event.clientX, y: event.clientY } });
        });

        document.addEventListener('scroll', function(event) {
            collectEvent({ type: 'scroll', data: { x: window.scrollX, y: window.scrollY } });
        });

        document.addEventListener('mousemove', function(event) {
            collectEvent({ type: 'mouse-move', data: { x: event.clientX, y: event.clientY } });
        });

        document.addEventListener('focus', function(event) {
            if (event.target.tagName === 'INPUT') {
                collectEvent({ type: 'form-field focus', data: { id: event.target.id } });
            }
        }, true);
        """
        return script

    def get_size(self) -> int:
        return len(self.get_script())

    def get_execution_time(self) -> float:
        # Simulate execution time
        return 10.0
