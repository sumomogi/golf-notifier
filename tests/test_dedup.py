import pytest
import json
import tempfile
import os
from datetime import date
from notifier.dedup import DedupTracker

@pytest.fixture
def log_file(tmp_path):
    return str(tmp_path / "sent_log.json")

def test_not_sent_initially(log_file):
    tracker = DedupTracker(log_file)
    assert not tracker.already_sent("event-123", date(2026, 4, 20), "week_before")

def test_mark_and_check(log_file):
    tracker = DedupTracker(log_file)
    tracker.mark_sent("event-123", date(2026, 4, 20), "week_before")
    assert tracker.already_sent("event-123", date(2026, 4, 20), "week_before")

def test_different_touchpoint_not_sent(log_file):
    tracker = DedupTracker(log_file)
    tracker.mark_sent("event-123", date(2026, 4, 20), "week_before")
    assert not tracker.already_sent("event-123", date(2026, 4, 20), "night_before")

def test_persists_across_instances(log_file):
    tracker1 = DedupTracker(log_file)
    tracker1.mark_sent("event-456", date(2026, 4, 26), "night_before")
    tracker2 = DedupTracker(log_file)
    assert tracker2.already_sent("event-456", date(2026, 4, 26), "night_before")
