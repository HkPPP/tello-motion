from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(slots=True)
class RuntimeConfig:
    dry_run_default: bool = True
    connect_timeout_s: int = 8
    log_level: str = "INFO"
    tello_wifi_ssid: str = "TELLO-9ABB41"
    tello_wifi_connect_timeout_s: float = 15.0


def load_runtime_config(path: Path) -> RuntimeConfig:
    defaults = RuntimeConfig()
    if not path.exists():
        return defaults

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    runtime = data.get("runtime", {})
    tello_wifi = data.get("tello_wifi", {})
    return RuntimeConfig(
        dry_run_default=bool(runtime.get("dry_run_default", defaults.dry_run_default)),
        connect_timeout_s=int(runtime.get("connect_timeout_s", defaults.connect_timeout_s)),
        log_level=str(runtime.get("log_level", defaults.log_level)).upper(),
        tello_wifi_ssid=str(tello_wifi.get("ssid", defaults.tello_wifi_ssid)),
        tello_wifi_connect_timeout_s=float(
            tello_wifi.get("connect_timeout_s", defaults.tello_wifi_connect_timeout_s)
        ),
    )
