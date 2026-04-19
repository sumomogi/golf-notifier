from datetime import date, timedelta


def get_touchpoints(event_date: date, today: date) -> list[str]:
    delta = (event_date - today).days
    result = []

    if delta == 1:
        result.append("night_before")
        return result  # night_before takes full priority

    if delta == 7:
        result.append("week_before")
        return result  # week_before on the exact 7-day mark; no weekend duplicate

    if today.weekday() in (5, 6):  # Saturday=5, Sunday=6
        # Check event is in the coming Mon-Fri
        days_until_next_monday = (7 - today.weekday()) % 7 or 7
        next_monday = today + timedelta(days=days_until_next_monday)
        next_friday = next_monday + timedelta(days=4)
        if next_monday <= event_date <= next_friday and delta > 1:
            result.append("weekend_before")

    return result
