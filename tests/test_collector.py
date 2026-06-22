import pytest
from collector import Collector, Event

def test_collector_collect():
    collector = Collector()
    event = Event('click', {'x': 10, 'y': 20})
    collector.collect(event)
    assert len(collector.events) == 1
    assert collector.events[0].type == 'click'
    assert collector.events[0].data == {'x': 10, 'y': 20}

def test_collector_store():
    collector = Collector()
    event = Event('click', {'x': 10, 'y': 20})
    collector.collect(event)
    db = {}
    collector.store(db)
    assert 'click' in db
    assert db['click'] == [{'x': 10, 'y': 20}]

def test_collector_get_script():
    collector = Collector()
    script = collector.get_script()
    assert len(script) < 30 * 1024  # 30 KB

def test_collector_get_size():
    collector = Collector()
    size = collector.get_size()
    assert size < 30 * 1024  # 30 KB

def test_collector_get_execution_time():
    collector = Collector()
    execution_time = collector.get_execution_time()
    assert execution_time < 20.0  # 20 ms
