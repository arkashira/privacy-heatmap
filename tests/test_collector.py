import pytest
from collector import Collector, Event, Database, generate_collector_script, get_collector_size, get_execution_time

def test_collector():
    collector = Collector()
    event = Event('click', {'x': 10, 'y': 20})
    collector.collect(event)
    db = Database()
    collector.store(db)
    assert len(db.events) == 1

def test_collector_script_size():
    size = get_collector_size()
    assert size < 30 * 1024  # 30 KB

def test_execution_time():
    time = get_execution_time()
    assert time < 20  # 20 ms

def test_event_types():
    collector = Collector()
    event_types = ['click', 'scroll', 'mouse-move', 'form-field focus']
    for event_type in event_types:
        event = Event(event_type, {})
        collector.collect(event)
    db = Database()
    collector.store(db)
    assert len(db.events) == len(event_types)

def test_edge_case_empty_event():
    collector = Collector()
    event = Event('', {})
    collector.collect(event)
    db = Database()
    collector.store(db)
    assert len(db.events) == 1
