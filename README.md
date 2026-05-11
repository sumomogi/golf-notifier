# Golf Notifier

Automatically sends an iMessage to someone when you have a golf appointment in Apple Calendar — so they know in advance you won't be available for the morning drop-off.

Runs silently in the background on macOS via launchd.

## How it works

- Checks your Apple Calendar daily at 8:50 PM
- Looks for events matching your configured `calendar_tag` (e.g. `"Golf"`) in the next 14 days
- Sends an iMessage at three touchpoints:
  - **7 days before** — `week_before`
  - **The weekend before** (Saturday or Sunday) — `weekend_before`
  - **The night before** — `night_before`
- Deduplicates: each message is sent only once per event per touchpoint

## Requirements

- macOS (uses Apple Calendar + Messages via AppleScript)
- Python 3.9+
- Contacts permission for Messages
- Calendar access permission

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/golf-notifier.git
   cd golf-notifier
   ```

2. Copy and edit the config:
   ```bash
   cp config.example.json config.json
   ```
   Fill in:
   - `recipient` — phone number in E.164 format (e.g. `+818012345678`)
   - `recipient_name` — just for your reference
   - `calendar_tag` — keyword to match in event title, notes, tags, or calendar name
   - `locale` — `"en"`, `"ja"`, or `"ko"` (controls weekday names and date format)
   - `messages` — customize the text for each touchpoint

3. Run setup (installs launchd job and sets Mac wake schedule):
   ```bash
   bash setup.sh
   ```

4. Test without sending:
   ```bash
   python3 check_golf_schedule.py --dry-run
   ```

## Configuration

```json
{
  "recipient": "+1XXXXXXXXXX",
  "recipient_name": "Your Recipient",
  "calendar_tag": "Golf",
  "lookahead_days": 14,
  "send_time": "20:50",
  "locale": "en",
  "messages": {
    "week_before": "Next {weekday} ({date}): I have golf, so no morning drop-off.",
    "weekend_before": "This {weekday} ({date}): I have golf, morning drop-off might not be possible.",
    "night_before": "Tomorrow ({date}): I have golf, so no morning drop-off."
  }
}
```

### Locale options

| `locale` | Weekday example | Date example |
|----------|-----------------|--------------|
| `en`     | Monday          | April 27     |
| `ja`     | 月曜日            | 4月27日       |
| `ko`     | 월요일            | 4월 27일      |

### Template variables

| Variable     | Description              |
|--------------|--------------------------|
| `{weekday}`  | Day of the week (localized) |
| `{date}`     | Event date (localized)   |

Note: `{weekday}` is not available in `night_before` by convention (you can still use it if you want).

## Running tests

```bash
python3 -m pytest tests/ -v
```

## File structure

```
golf_notifier/
├── check_golf_schedule.py      # Main entry point
├── config.example.json         # Config template (copy to config.json)
├── golf-notifier.plist.template  # launchd template (setup.sh fills this in)
├── setup.sh                    # One-time setup script
├── notifier/
│   ├── calendar.py             # Reads Apple Calendar via AppleScript
│   ├── composer.py             # Formats messages with locale support
│   ├── sender.py               # Sends iMessage via AppleScript
│   ├── dedup.py                # Prevents duplicate sends
│   └── touchpoints.py          # Determines which touchpoints apply today
└── tests/
```

## License

MIT
