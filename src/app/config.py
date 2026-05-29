from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(slots=True)
class RuntimeConfig:
    dry_run_default: bool = True
    connect_timeout_s: int = 8
    log_level: str = "INFO"


def load_runtime_config(path: Path) -> RuntimeConfig:
    if not path.exists():
        return RuntimeConfig()

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    runtime = data.get("runtime", {})
    return RuntimeConfig(
        dry_run_default=bool(runtime.get("dry_run_default", True)),
        connect_timeout_s=int(runtime.get("connect_timeout_s", 8)),
        log_level=str(runtime.get("log_level", "INFO")).upper(),
    )
