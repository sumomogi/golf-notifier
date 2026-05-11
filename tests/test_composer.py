import pytest
from datetime import date
from notifier.composer import compose

TEMPLATES = {
    "week_before": "Next {weekday} ({date}): golf, no morning drop-off.",
    "weekend_before": "This {weekday} ({date}): golf, morning drop-off might not be possible.",
    "night_before": "Tomorrow ({date}): golf, no morning drop-off.",
}

TEMPLATES_JA = {
    "week_before": "来週{weekday}（{date}）はゴルフのため送迎できません。",
    "weekend_before": "今週{weekday}（{date}）はゴルフのため送迎できない可能性があります。",
    "night_before": "明日（{date}）はゴルフのため送迎できません。",
}

TEMPLATES_KO = {
    "week_before": "다음 주 {weekday} ({date})에 골프가 있어서 아침에 데려다 드리기 어렵습니다.",
    "weekend_before": "이번 주 {weekday} ({date})에 골프가 있어서 아침 픽업이 어려울 수 있습니다.",
    "night_before": "내일 ({date})에 골프가 있어서 아침에 데려다 드리지 못합니다.",
}


def test_week_before_english():
    msg = compose("week_before", date(2026, 4, 27), TEMPLATES, locale="en")
    assert "Monday" in msg
    assert "April 27" in msg


def test_night_before_english():
    msg = compose("night_before", date(2026, 4, 27), TEMPLATES, locale="en")
    assert "April 27" in msg
    assert "{weekday}" not in msg
    assert "{date}" not in msg


def test_weekend_before_english():
    msg = compose("weekend_before", date(2026, 4, 29), TEMPLATES, locale="en")
    assert "Wednesday" in msg
    assert "April 29" in msg


def test_week_before_japanese():
    msg = compose("week_before", date(2026, 4, 27), TEMPLATES_JA, locale="ja")
    assert "月曜日" in msg
    assert "4月27日" in msg


def test_weekend_before_japanese():
    msg = compose("weekend_before", date(2026, 4, 29), TEMPLATES_JA, locale="ja")
    assert "水曜日" in msg
    assert "4月29日" in msg


def test_week_before_korean():
    msg = compose("week_before", date(2026, 4, 27), TEMPLATES_KO, locale="ko")
    assert "월요일" in msg
    assert "4월 27일" in msg


def test_weekend_before_korean():
    msg = compose("weekend_before", date(2026, 4, 29), TEMPLATES_KO, locale="ko")
    assert "수요일" in msg
    assert "4월 29일" in msg


def test_unknown_locale_falls_back_to_english():
    msg = compose("week_before", date(2026, 4, 27), TEMPLATES, locale="fr")
    assert "Monday" in msg


def test_unknown_touchpoint_raises():
    with pytest.raises(KeyError):
        compose("nonexistent", date(2026, 4, 27), TEMPLATES)
