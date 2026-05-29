from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FollowController:
    enabled: bool = False
