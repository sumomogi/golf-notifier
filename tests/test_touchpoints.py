import pytest
from datetime import date
from notifier.touchpoints import get_touchpoints

def test_week_before():
    event = date(2026, 4, 27)
    today = date(2026, 4, 20)  # exactly 7 days before
    assert get_touchpoints(event, today) == ["week_before"]

def test_night_before():
    event = date(2026, 4, 27)
    today = date(2026, 4, 26)
    assert get_touchpoints(event, today) == ["night_before"]

def test_weekend_before_saturday():
    event = date(2026, 4, 29)  # Wednesday
    today = date(2026, 4, 25)  # Saturday of the preceding week
    assert get_touchpoints(event, today) == ["weekend_before"]

def test_weekend_before_sunday():
    event = date(2026, 4, 29)  # Wednesday
    today = date(2026, 4, 26)  # Sunday of the preceding week
    assert get_touchpoints(event, today) == ["weekend_before"]

def test_no_touchpoint():
    event = date(2026, 4, 30)
    today = date(2026, 4, 20)  # 10 days before, no trigger
    assert get_touchpoints(event, today) == []

def test_week_before_on_weekend_no_duplicate():
    # Event is exactly 7 days away AND today is Saturday — only week_before fires
    event = date(2026, 4, 25)  # Saturday
    today = date(2026, 4, 18)  # Saturday, exactly 7 days before
    result = get_touchpoints(event, today)
    assert result == ["week_before"]
    assert "weekend_before" not in result

def test_night_before_takes_priority_over_weekend():
    # Event is tomorrow AND today is Sunday — night_before only
    event = date(2026, 4, 27)  # Monday
    today = date(2026, 4, 26)  # Sunday
    result = get_touchpoints(event, today)
    assert "night_before" in result
    assert "weekend_before" not in result
