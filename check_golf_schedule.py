#!/usr/bin/env python3
# ~/golf_notifier/check_golf_schedule.py
import json
import sys
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from notifier.calendar import fetch_golf_events
from notifier.touchpoints import get_touchpoints
from notifier.composer import compose
from notifier.dedup import DedupTracker
from notifier.sender import send_imessage

def main():
    dry_run = "--dry-run" in sys.argv

    config_path = os.path.join(BASE_DIR, "config.json")
    with open(config_path) as f:
        config = json.load(f)

    log_path = os.path.join(BASE_DIR, "sent_log.json")
    tracker = DedupTracker(log_path)
    today = date.today()

    events = fetch_golf_events(config["calendar_tag"], config["lookahead_days"])
    print(f"[{today}] Found {len(events)} golf event(s) in next {config['lookahead_days']} days.")

    for event in events:
        touchpoints = get_touchpoints(event["date"], today)
        for tp in touchpoints:
            if tracker.already_sent(event["id"], today, tp):
                print(f"  SKIP (already sent): {event['title']} on {event['date']} [{tp}]")
                continue
            message = compose(tp, event["date"], config["messages"])
            print(f"  SEND [{tp}] to {config['recipient']}: {message}")
            if not dry_run:
                send_imessage(config["recipient"], message)
                tracker.mark_sent(event["id"], today, tp)
            else:
                print("  (dry-run: not actually sent)")

if __name__ == "__main__":
    main()
