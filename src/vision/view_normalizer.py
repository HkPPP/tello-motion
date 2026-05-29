from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ViewNormalizer:
    model_ready: bool = False
