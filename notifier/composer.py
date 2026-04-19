from datetime import date

WEEKDAYS_JA = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

def compose(touchpoint: str, event_date: date, templates: dict) -> str:
    weekday = WEEKDAYS_JA[event_date.weekday()]
    date_str = f"{event_date.month}月{event_date.day}日"
    template = templates[touchpoint]
    return template.format(weekday=weekday, date=date_str)
