import pytest
from io import StringIO
from unittest.mock import MagicMock
from privacy_heatmap import PrivacyHeatmap, Event

@pytest.fixture
def db_connection():
    class MockDBConnection:
        def __init__(self):
            self.execute_calls = []

        def execute(self, query, params):
            self.execute_calls.append((query, params))

    return MockDBConnection()

def test_capture_event():
    heatmap = PrivacyHeatmap()
    event_type = "click"
    event_data = {"x": 10, "y": 20}
    heatmap.capture_event(event_type, event_data)
    assert len(heatmap.events) == 1
    assert heatmap.events[0].event_type == event_type
    assert heatmap.events[0].event_data == event_data

def test_post_events():
    heatmap = PrivacyHeatmap()
    event_type = "click"
    event_data = {"x": 10, "y": 20}
    heatmap.capture_event(event_type, event_data)
    endpoint = "https://example.com/endpoint"
    posted_data = heatmap.post_events(endpoint)
    assert posted_data == '[{"event_type": "click", "event_data": {"x": 10, "y": 20}}]'

def test_persist_events(db_connection):
    heatmap = PrivacyHeatmap()
    event_type = "click"
    event_data = {"x": 10, "y": 20}
    heatmap.capture_event(event_type, event_data)
    heatmap.persist_events(db_connection)
    assert len(db_connection.execute_calls) == 1
    assert db_connection.execute_calls[0][0] == "INSERT INTO wp_privacy_heatmap_events (event_type, event_data) VALUES (%s, %s)"
    assert db_connection.execute_calls[0][1] == ("click", '{"x": 10, "y": 20}')

def test_post_events_empty():
    heatmap = PrivacyHeatmap()
    endpoint = "https://example.com/endpoint"
    posted_data = heatmap.post_events(endpoint)
    assert posted_data == '[]'

def test_persist_events_empty(db_connection):
    heatmap = PrivacyHeatmap()
    heatmap.persist_events(db_connection)
    assert len(db_connection.execute_calls) == 0
