from privacy_heatmap import PrivacyHeatmap, AuditLog
import json
from datetime import datetime, timedelta

def test_log_access():
    heatmap = PrivacyHeatmap()
    heatmap.log_access(1, "read")
    assert len(heatmap.audit_log) == 1
    assert heatmap.audit_log[0].user_id == 1
    assert heatmap.audit_log[0].action == "read"

def test_prune_log():
    heatmap = PrivacyHeatmap(log_retention=1)
    heatmap.log_access(1, "read")
    heatmap.audit_log[0].timestamp = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    heatmap._prune_log()
    assert len(heatmap.audit_log) == 0

def test_export_log():
    heatmap = PrivacyHeatmap()
    heatmap.log_access(1, "read")
    heatmap.log_access(2, "write")
    log_json = heatmap.export_log()
    log_data = json.loads(log_json)
    assert len(log_data) == 2
    assert log_data[0]["user_id"] == 1
    assert log_data[0]["action"] == "read"
    assert log_data[1]["user_id"] == 2
    assert log_data[1]["action"] == "write"

def test_log_retention():
    heatmap = PrivacyHeatmap(log_retention=1)
    heatmap.log_access(1, "read")
    heatmap.audit_log[0].timestamp = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    heatmap._prune_log()
    assert len(heatmap.audit_log) == 0
