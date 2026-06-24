import pytest
from datetime import datetime, timedelta
from privacy_heatmap import PrivacyHeatmap, LogEntry

@pytest.fixture
def heatmap():
    return PrivacyHeatmap()

def test_purge_records(heatmap):
    heatmap.add_record({'timestamp': datetime.now() - timedelta(days=91)})
    heatmap.add_record({'timestamp': datetime.now() - timedelta(days=89)})
    assert heatmap.purge_records() == 1
    assert len(heatmap.get_log()) == 1

def test_purge_records_edge_case(heatmap):
    heatmap.add_record({'timestamp': datetime.now() - timedelta(days=90)})
    assert heatmap.purge_records() == 1
    assert len(heatmap.get_log()) == 1

def test_set_retention_days(heatmap):
    heatmap.set_retention_days(60)
    assert heatmap.retention_days == 60

def test_log_entry(heatmap):
    heatmap.add_record({'timestamp': datetime.now() - timedelta(days=91)})
    heatmap.purge_records()
    log_entry = heatmap.get_log()[0]
    assert isinstance(log_entry, LogEntry)
    assert log_entry.timestamp >= datetime.now() - timedelta(minutes=1)
    assert log_entry.records_purged == 1
