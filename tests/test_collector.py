from collector import Collector, Event, Database, generate_collector_script, get_collector_size, get_execution_time
import pytest

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
    event_types = ['click', 'scroll', 'mousemove', 'focus']
    for event_type in event_types:
        event = Event(event_type, {'data': 'test'})
        collector.collect(event)
    db = Database()
    collector.store(db)
    assert len(db.events) == len(event_types)

def test_database_store():
    db = Database()
    event = Event('click', {'x': 10, 'y': 20})
    db.store(event)
    assert len(db.events) == 1
