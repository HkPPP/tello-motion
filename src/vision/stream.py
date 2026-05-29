from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VideoStream:
    enabled: bool = False
