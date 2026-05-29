from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class TrickStep:
    command: str
    value: int | None = None


class TrickPlugin(Protocol):
    name: str

    def plan_steps(self) -> list[TrickStep]:
        ...
