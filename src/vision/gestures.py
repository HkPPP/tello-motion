from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GestureRecognizer:
    enabled: bool = False
