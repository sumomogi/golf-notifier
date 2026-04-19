# ~/golf_notifier/notifier/calendar.py
import subprocess
import json
from datetime import date, timedelta

def fetch_golf_events(tag: str, lookahead_days: int) -> list[dict]:
    """
    Returns list of dicts: [{"id": str, "date": date, "title": str}, ...]
    Queries Apple Calendar via AppleScript for events in the next lookahead_days
    whose notes or title contain the tag string.
    """
    today = date.today()
    end = today + timedelta(days=lookahead_days)

    script = f"""
    set tagToFind to "{tag}"
    set startDate to current date
    set startDate to (startDate - (time of startDate))
    set endDate to startDate + ({lookahead_days} * days)

    set resultList to {{}}

    tell application "Calendar"
        repeat with cal in calendars
            set evts to (every event of cal whose start date >= startDate and start date <= endDate)
            repeat with evt in evts
                set evtTitle to summary of evt
                set evtNotes to ""
                try
                    set evtNotes to description of evt
                end try
                set evtTags to ""
                try
                    -- tags stored as comma-separated string in tag list
                    set tagItems to tags of evt
                    repeat with t in tagItems
                        set evtTags to evtTags & name of t & ","
                    end repeat
                end try
                if evtTags contains tagToFind or evtNotes contains tagToFind or evtTitle contains tagToFind then
                    set evtDate to start date of evt
                    set evtUid to uid of evt
                    set end of resultList to (evtUid & "|" & (year of evtDate as text) & "-" & (month of evtDate as integer as text) & "-" & (day of evtDate as text) & "|" & evtTitle)
                end if
            end repeat
        end repeat
    end tell

    set AppleScript's text item delimiters to linefeed
    return resultList as text
    """

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Calendar query failed: {result.stderr}")

    events = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) < 3:
            continue
        uid, date_str, title = parts[0], parts[1], parts[2]
        try:
            y, m, d = date_str.split("-")
            evt_date = date(int(y), int(m), int(d))
        except ValueError:
            continue
        events.append({"id": uid, "date": evt_date, "title": title})

    return events
