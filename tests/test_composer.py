import pytest
from datetime import date
from notifier.composer import compose

TEMPLATES = {
    "week_before": "【お知らせ】来週{weekday}（{date}）はゴルフの予定があるため、7:45の駅への送迎が難しい見込みです。ご確認ください。",
    "weekend_before": "【お知らせ】今週{weekday}（{date}）はゴルフの予定があるため、朝の送迎ができない可能性があります。事前にご準備をお願いします。",
    "night_before": "【お知らせ】明日（{date}）はゴルフの予定があるため、7:45の駅への送迎は対応できません。お手数ですが自力でのご移動をお願いします。",
}

def test_week_before_message():
    event = date(2026, 4, 27)  # Monday
    msg = compose("week_before", event, TEMPLATES)
    assert "来週月曜日" in msg
    assert "4月27日" in msg
    assert "【お知らせ】" in msg

def test_night_before_message():
    event = date(2026, 4, 27)
    msg = compose("night_before", event, TEMPLATES)
    assert "明日" in msg
    assert "4月27日" in msg
    assert "{weekday}" not in msg
    assert "{date}" not in msg

def test_weekend_before_message():
    event = date(2026, 4, 29)  # Wednesday
    msg = compose("weekend_before", event, TEMPLATES)
    assert "今週水曜日" in msg
    assert "4月29日" in msg

def test_unknown_touchpoint_raises():
    with pytest.raises(KeyError):
        compose("nonexistent", date(2026, 4, 27), TEMPLATES)
