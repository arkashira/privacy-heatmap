from wordpress_plugin import WordPressPlugin, UserInteraction

def test_track_mouse_movements():
    plugin = WordPressPlugin()
    plugin.track_mouse_movements([(1, 2), (3, 4)])
    assert len(plugin.interactions) == 1
    assert plugin.interactions[0].mouse_movements == [(1, 2), (3, 4)]

def test_track_clicks():
    plugin = WordPressPlugin()
    plugin.track_clicks([(5, 6), (7, 8)])
    assert len(plugin.interactions) == 1
    assert plugin.interactions[0].clicks == [(5, 6), (7, 8)]

def test_track_scrolls():
    plugin = WordPressPlugin()
    plugin.track_scrolls([(9, 10), (11, 12)])
    assert len(plugin.interactions) == 1
    assert plugin.interactions[0].scrolls == [(9, 10), (11, 12)]

def test_anonymize_ip_device_data():
    plugin = WordPressPlugin()
    anonymized_ip, anonymized_device = plugin.anonymize_ip_device_data("192.168.1.1", "Desktop")
    assert anonymized_ip == "anonymized_ip"
    assert anonymized_device == "anonymized_device"

def test_store_raw_events():
    plugin = WordPressPlugin()
    events = [UserInteraction([(1, 2), (3, 4)], [], []), UserInteraction([], [(5, 6), (7, 8)], [])]
    plugin.store_raw_events(events)
    assert plugin.events == events

def test_send_anonymized_session_data():
    plugin = WordPressPlugin()
    events = [UserInteraction([(1, 2), (3, 4)], [], []), UserInteraction([], [(5, 6), (7, 8)], [])]
    anonymized_events = plugin.send_anonymized_session_data(events)
    assert len(anonymized_events) == 2
    assert anonymized_events[0]["mouse_movements"] == [(1, 2), (3, 4)]
    assert anonymized_events[0]["ip"] == "anonymized_ip"
    assert anonymized_events[0]["device"] == "anonymized_device"
    assert anonymized_events[1]["clicks"] == [(5, 6), (7, 8)]
    assert anonymized_events[1]["ip"] == "anonymized_ip"
    assert anonymized_events[1]["device"] == "anonymized_device"
