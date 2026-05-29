from __future__ import annotations

import logging
import re
import subprocess
import time
from dataclasses import dataclass, field

LOGGER = logging.getLogger("tello_motion.tello_wifi")

_SSID_PATTERN = re.compile(r"^\s*SSID\s*:\s*(.+)$", re.MULTILINE)


def _run_netsh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["netsh", "wlan", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def get_connected_ssid() -> str | None:
    result = _run_netsh("show", "interfaces")
    if result.returncode != 0:
        LOGGER.debug("netsh wlan show interfaces failed: %s", result.stderr.strip())
        return None

    match = _SSID_PATTERN.search(result.stdout)
    if not match:
        return None

    ssid = match.group(1).strip()
    if not ssid or ssid.lower() == "n/a":
        return None
    return ssid


@dataclass(slots=True)
class TelloWifiSession:
    ssid: str
    connect_timeout_s: float = 15.0
    _previous_ssid: str | None = field(default=None, init=False)
    _connected: bool = field(default=False, init=False)
    _switch_attempted: bool = field(default=False, init=False)

    def connect(self) -> bool:
        current_ssid = get_connected_ssid()
        if current_ssid == self.ssid:
            LOGGER.info("Already connected to Tello WiFi %s.", self.ssid)
            self._connected = True
            return True

        self._previous_ssid = current_ssid
        if self._previous_ssid:
            LOGGER.info("Saving current WiFi network: %s", self._previous_ssid)

        LOGGER.info("Connecting to Tello WiFi %s...", self.ssid)
        self._switch_attempted = True
        result = _run_netsh("connect", f"name={self.ssid}")
        if result.returncode != 0:
            LOGGER.error(
                "Failed to connect to %s. Ensure the network profile exists in Windows. netsh: %s",
                self.ssid,
                (result.stderr or result.stdout).strip(),
            )
            return False

        deadline = time.monotonic() + self.connect_timeout_s
        while time.monotonic() < deadline:
            if get_connected_ssid() == self.ssid:
                LOGGER.info("Connected to Tello WiFi %s.", self.ssid)
                self._connected = True
                return True
            time.sleep(0.5)

        LOGGER.error(
            "Timed out after %.0fs waiting for connection to %s.",
            self.connect_timeout_s,
            self.ssid,
        )
        return False

    def disconnect(self) -> None:
        if not self._connected and not self._switch_attempted:
            return

        if self._previous_ssid and self._previous_ssid != self.ssid:
            LOGGER.info("Restoring previous WiFi network: %s", self._previous_ssid)
            result = _run_netsh("connect", f"name={self._previous_ssid}")
            if result.returncode != 0:
                LOGGER.warning(
                    "Failed to restore %s; disconnecting from Tello WiFi instead. netsh: %s",
                    self._previous_ssid,
                    (result.stderr or result.stdout).strip(),
                )
                _run_netsh("disconnect")
            else:
                LOGGER.info("Restored previous WiFi network.")
        else:
            LOGGER.info("Disconnecting from Tello WiFi %s.", self.ssid)
            _run_netsh("disconnect")

        self._connected = False
        self._switch_attempted = False

    def __enter__(self) -> TelloWifiSession:
        if not self.connect():
            raise RuntimeError(f"Unable to connect to Tello WiFi {self.ssid}.")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.disconnect()
