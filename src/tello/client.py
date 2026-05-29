from __future__ import annotations

import logging

LOGGER = logging.getLogger("tello_motion.tello_client")


class TelloClient:
    def __init__(self, dry_run: bool, connect_timeout_s: int = 8) -> None:
        self._dry_run = dry_run
        self._connect_timeout_s = connect_timeout_s
        self._client: object | None = None

    def connect(self) -> bool:
        if self._dry_run:
            LOGGER.info("Dry-run mode enabled; skipping real drone connection.")
            return True

        try:
            from djitellopy import Tello

            self._client = Tello()
            self._client.RESPONSE_TIMEOUT = self._connect_timeout_s
            self._client.connect()
            LOGGER.info("Connected to Tello successfully.")
            return True
        except Exception as exc:  # pragma: no cover - network/device-dependent
            LOGGER.exception("Tello connection failed: %s", exc)
            return False
