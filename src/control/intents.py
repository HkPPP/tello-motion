from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntentType(str, Enum):
    TAKEOFF = "takeoff"
    LAND = "land"
    FOLLOW_LOCK = "follow_lock"
    FOLLOW_UNLOCK = "follow_unlock"
    TRICK = "trick"


@dataclass(slots=True)
class Intent:
    intent_type: IntentType
    payload: dict[str, object]


@dataclass(slots=True)
class IntentMapper:
    enabled: bool = False
