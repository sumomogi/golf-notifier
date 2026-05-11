from datetime import date

WEEKDAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "ja": ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"],
    "ko": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
}

DATE_FORMAT = {
    "en": lambda d: f"{d.strftime('%B')} {d.day}",
    "ja": lambda d: f"{d.month}月{d.day}日",
    "ko": lambda d: f"{d.month}월 {d.day}일",
}


def compose(touchpoint: str, event_date: date, templates: dict, locale: str = "en") -> str:
    weekdays = WEEKDAYS.get(locale, WEEKDAYS["en"])
    fmt = DATE_FORMAT.get(locale, DATE_FORMAT["en"])
    weekday = weekdays[event_date.weekday()]
    date_str = fmt(event_date)
    if touchpoint not in templates:
        raise KeyError(f"No template for touchpoint '{touchpoint}'. Available: {list(templates.keys())}")
    return templates[touchpoint].format(weekday=weekday, date=date_str)
