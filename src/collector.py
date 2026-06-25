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

    def store(self, db):
        for event in self.events:
            db.store(event)

class Database:
    def __init__(self):
        self.events = []

    def store(self, event: Event):
        self.events.append(event)

def generate_collector_script():
    return """
    // Lightweight JavaScript collector
    function collectEvent(event) {
        // Send event to server
        fetch('/collect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        });
    }

    // Add event listeners
    document.addEventListener('click', (e) => {
        collectEvent({ type: 'click', data: { x: e.clientX, y: e.clientY } });
    });

    document.addEventListener('scroll', (e) => {
        collectEvent({ type: 'scroll', data: { x: window.scrollX, y: window.scrollY } });
    });

    document.addEventListener('mousemove', (e) => {
        collectEvent({ type: 'mousemove', data: { x: e.clientX, y: e.clientY } });
    });

    document.addEventListener('focus', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            collectEvent({ type: 'focus', data: { element: e.target.name } });
        }
    }, true);
    """

def get_collector_size():
    script = generate_collector_script()
    return len(script.encode('utf-8'))

def get_execution_time():
    # Simulate execution time
    return 10
