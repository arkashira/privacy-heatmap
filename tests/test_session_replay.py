import pytest
from session_replay import SessionReplay, SessionEvent
from datetime import datetime, timedelta
import time

def test_session_replay_loads_within_3_seconds():
    session_events = [
        SessionEvent(datetime.now(), "mouse_move", {"x": 10, "y": 20}),
        SessionEvent(datetime.now() + timedelta(seconds=1), "click", {"x": 30, "y": 40}),
    ]
    replay = SessionReplay(session_events)
    start_time = time.time()
    replay.load()
    end_time = time.time()
    assert end_time - start_time < 3

def test_session_replay_includes_mouse_movements_clicks_and_scrolls():
    session_events = [
        SessionEvent(datetime.now(), "mouse_move", {"x": 10, "y": 20}),
        SessionEvent(datetime.now() + timedelta(seconds=1), "click", {"x": 30, "y": 40}),
        SessionEvent(datetime.now() + timedelta(seconds=2), "scroll", {"x": 50, "y": 60}),
    ]
    replay = SessionReplay(session_events)
    events = list(replay.play())
    assert len(events) == 3
    assert events[0].event_type == "mouse_move"
    assert events[1].event_type == "click"
    assert events[2].event_type == "scroll"

def test_session_replay_can_be_paused_resumed_and_scrubbed():
    session_events = [
        SessionEvent(datetime.now(), "mouse_move", {"x": 10, "y": 20}),
        SessionEvent(datetime.now() + timedelta(seconds=1), "click", {"x": 30, "y": 40}),
    ]
    replay = SessionReplay(session_events)
    replay.play()
    replay.pause()
    assert not replay.playing
    replay.resume()
    assert replay.playing
    replay.scrub(0.5)
    assert replay.current_time == 0.5
    assert not replay.playing
