import json
import os
from datetime import date

class DedupTracker:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self._data: dict = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.log_path):
            return {}
        with open(self.log_path) as f:
            return json.load(f)

    def _save(self):
        with open(self.log_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def _key(self, event_id: str, today: date, touchpoint: str) -> str:
        return f"{event_id}:{today.isoformat()}:{touchpoint}"

    def already_sent(self, event_id: str, today: date, touchpoint: str) -> bool:
        return self._key(event_id, today, touchpoint) in self._data

    def mark_sent(self, event_id: str, today: date, touchpoint: str):
        self._data[self._key(event_id, today, touchpoint)] = True
        self._save()
