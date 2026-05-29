from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SafetyController:
    armed: bool = False
    emergency_stopped: bool = False
