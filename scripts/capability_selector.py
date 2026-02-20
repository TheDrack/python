# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path
from typing import List, Dict


CAPABILITY_FILE = Path("docs/capability.json")


class CapabilitySelector:
    def __init__(self, path: Path = CAPABILITY_FILE):
        if not path.exists():
            raise FileNotFoundError(f"Capability file not found: {path}")
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _completed_ids(self) -> set:
        return {
            cap["id"]
            for cap in self.data["capabilities"]
            if cap["status"] == "completed"
        }

    def _dependencies_satisfied(self, cap: Dict, completed: set) -> bool:
        return all(dep in completed for dep in cap.get("depends_on", []))

    def select_next(self) -> Dict | None:
        completed = self._completed_ids()

        candidates: List[Dict] = [
            cap for cap in self.data["capabilities"]
            if cap["status"] == "pending"
            and cap.get("auto", False) is True
            and self._dependencies_satisfied(cap, completed)
        ]

        if not candidates:
            return None

        # prioridade menor = mais importante
        candidates.sort(key=lambda c: (c.get("priority", 999), c["id"]))

        return candidates[0]


if __name__ == "__main__":
    selector = CapabilitySelector()
    capability = selector.select_next()

    if not capability:
        print("NO_CAPABILITY")
        sys.exit(0)

    # saída limpa para GitHub Actions
    print(json.dumps({
        "id": capability["id"],
        "title": capability["title"],
        "description": capability["description"],
        "notes": capability.get("notes", "")
    }))