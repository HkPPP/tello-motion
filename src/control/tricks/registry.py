from __future__ import annotations

from dataclasses import dataclass, field

from src.control.tricks.base import TrickPlugin


@dataclass(slots=True)
class TrickRegistry:
    _plugins: dict[str, TrickPlugin] = field(default_factory=dict)

    def register(self, plugin: TrickPlugin) -> None:
        self._plugins[plugin.name] = plugin

    def names(self) -> list[str]:
        return sorted(self._plugins.keys())
