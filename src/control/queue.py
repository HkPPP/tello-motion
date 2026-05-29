from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from src.control.intents import Intent


@dataclass(slots=True)
class ActionQueue:
    _items: deque[Intent] = field(default_factory=deque)

    def push(self, intent: Intent) -> None:
        self._items.append(intent)

    def pop(self) -> Intent | None:
        if not self._items:
            return None
        return self._items.popleft()
