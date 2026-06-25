import pytest
from analytics_engine import AnalyticsEngine, VisitorEvent
import sqlite3
import json
from datetime import datetime, timedelta

@pytest.fixture
def engine():
    db_path = ":memory:"
    retention_days = 30
    return AnalyticsEngine(db_path, retention_days)

def test_store_event(engine):
    event = VisitorEvent(1, datetime.now(), {"key": "value"})
    engine.store_event(event)
    engine.cursor.execute("SELECT * FROM visitor_events")
    result = engine.cursor.fetchone()
    assert result[0] == 1
    assert result[1] == event.timestamp.isoformat()
    assert json.loads(result[2]) == event.data

def test_delete_old_data(engine):
    event1 = VisitorEvent(1, datetime.now(), {"key": "value"})
    event2 = VisitorEvent(2, datetime.now() - timedelta(days=31), {"key": "value"})
    engine.store_event(event1)
    engine.store_event(event2)
    engine.delete_old_data()
    engine.cursor.execute("SELECT * FROM visitor_events")
    result = engine.cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == 1

def test_close(engine):
    engine.close()
    with pytest.raises(sqlite3.ProgrammingError):
        engine.cursor.execute("SELECT * FROM visitor_events")
