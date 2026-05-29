from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.app.config import RuntimeConfig, load_runtime_config
from src.control.executor import CommandExecutor
from src.control.follow_mode import FollowController
from src.control.intents import IntentMapper
from src.control.queue import ActionQueue
from src.control.tricks.registry import TrickRegistry
from src.tello.client import TelloClient
from src.tello.safety import SafetyController
from src.tello.wifi import TelloWifiSession
from src.vision.gestures import GestureRecognizer
from src.vision.stream import VideoStream
from src.vision.tracking import PersonTracker
from src.vision.view_normalizer import ViewNormalizer


LOGGER = logging.getLogger("tello_motion")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="tello-motion bootstrap runtime")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without sending commands to an actual drone.",
    )
    parser.add_argument(
        "--config",
        default="config/runtime.toml",
        help="Path to runtime TOML config file.",
    )
    return parser


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def _initialize_modules(config: RuntimeConfig, dry_run: bool) -> dict[str, object]:
    tello_client = TelloClient(dry_run=dry_run, connect_timeout_s=config.connect_timeout_s)
    modules: dict[str, object] = {
        "tello_client": tello_client,
        "safety_controller": SafetyController(),
        "video_stream": VideoStream(),
        "view_normalizer": ViewNormalizer(),
        "gesture_recognizer": GestureRecognizer(),
        "person_tracker": PersonTracker(),
        "intent_mapper": IntentMapper(),
        "action_queue": ActionQueue(),
        "command_executor": CommandExecutor(),
        "follow_controller": FollowController(),
        "trick_registry": TrickRegistry(),
    }
    LOGGER.info("Initialized modules: %s", ", ".join(modules.keys()))
    return modules


def run() -> int:
    args = _build_parser().parse_args()
    config = load_runtime_config(Path(args.config))
    _configure_logging(config.log_level)
    dry_run = args.dry_run or config.dry_run_default

    wifi_session: TelloWifiSession | None = None
    if not dry_run:
        wifi_session = TelloWifiSession(
            ssid=config.tello_wifi_ssid,
            connect_timeout_s=config.tello_wifi_connect_timeout_s,
        )

    try:
        if wifi_session is not None and not wifi_session.connect():
            LOGGER.error("Unable to connect to Tello WiFi.")
            return 1

        modules = _initialize_modules(config, dry_run=dry_run)
        tello_client = modules["tello_client"]
        assert isinstance(tello_client, TelloClient)

        if not tello_client.connect():
            LOGGER.error("Unable to initialize Tello connection.")
            return 1

        LOGGER.info("Phase 1 bootstrap completed successfully.")
        return 0
    finally:
        if wifi_session is not None:
            wifi_session.disconnect()
