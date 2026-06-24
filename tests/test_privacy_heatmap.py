import pytest
from privacy_heatmap import Event, LocalDataCollectionEngine

def test_capture_event():
    engine = LocalDataCollectionEngine()
    event = Event('click', 10, 20, 50)
    engine.capture_event(event)
    assert len(engine.events) == 1
    assert engine.events[0].event_type == 'click'

def test_post_events():
    engine = LocalDataCollectionEngine()
    event = Event('click', 10, 20, 50)
    engine.capture_event(event)
    posted_events = engine.post_events('https://example.com/endpoint')
    assert posted_events == '[{"event_type": "click", "x": 10, "y": 20, "scroll_depth": 50}]'

def test_persist_events():
    engine = LocalDataCollectionEngine()
    event = Event('click', 10, 20, 50)
    engine.capture_event(event)
    db = {}
    persisted_db = engine.persist_events(db)
    assert persisted_db['events'] == [{'event_type': 'click', 'x': 10, 'y': 20, 'scroll_depth': 50}]

def test_main():
    engine = LocalDataCollectionEngine()
    posted_events, persisted_db = engine.main()
    assert posted_events == '[{"event_type": "click", "x": 10, "y": 20, "scroll_depth": 50}, {"event_type": "scroll", "x": 30, "y": 40, "scroll_depth": 60}]'
    assert persisted_db['events'] == [{'event_type': 'click', 'x': 10, 'y': 20, 'scroll_depth': 50}, {'event_type': 'scroll', 'x': 30, 'y': 40, 'scroll_depth': 60}]
