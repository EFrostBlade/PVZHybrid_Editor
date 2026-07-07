"""Runtime path and title helpers for the PVZ Hybrid editor."""
# ruff: noqa: UP007,UP045

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

PathInput = Union[str, Path]
DEFAULT_GAME_VERSION = "Game not found"
BLOCKED_UPDATE_RESPONSE = "The content may contain violation information"
LEGACY_UPDATE_VERSION = "0.74"
GAME_VERSION_MARKERS = (
    ("v3.13.2", 3.132),
    ("v3.9.9", 3.99),
    ("v3.7.6", 3.76),
    ("v3.7.5", 3.75),
    ("v3.6.5", 3.65),
    ("v3.2.1", 3.21),
    ("v3.1.5", 3.15),
    ("v2.6.1", 2.61),
    ("v2.3.7", 2.37),
    ("v2.3.6", 2.36),
    ("v2.3.5", 2.35),
    ("v3.17", 3.17),
    ("v3.16", 3.16),
    ("v3.15", 3.151),
    ("v3.14", 3.14),
    ("v3.12", 3.12),
    ("v3.11", 3.11),
    ("v3.10", 3.10),
    ("v3.9", 3.9),
    ("v3.8", 3.8),
    ("v3.7", 3.7),
    ("v3.6", 3.6),
    ("v3.5", 3.5),
    ("v3.4", 3.4),
    ("v3.3", 3.3),
    ("v3.2", 3.2),
    ("v3.1", 3.1),
    ("v3.0", 3.0),
    ("v2.6", 2.6),
    ("v2.5", 2.5),
    ("v2.4", 2.4),
    ("v2.3", 2.3),
    ("v2.2", 2.2),
    ("v2.1", 2.1),
    ("v2.0", 2.0),
)


@dataclass(frozen=True)
class RunningGameProcess:
    process_id: int
    window_title: str
    detected_version: Optional[float]
    memory: Any
    process_name: str


@dataclass(frozen=True)
class UpdateDecision:
    latest_version: str
    is_blocked: bool
    should_open_update_window: bool


class GameProcessNotFound(LookupError):
    pass


def resource_path(
    relative_path: PathInput,
    *,
    runtime: Any = None,
    base_dir: Optional[PathInput] = None,
) -> str:
    if base_dir is None:
        bundle_dir = getattr(runtime, "_MEIPASS", None)
        base_path = Path(bundle_dir) if bundle_dir else Path(os.path.abspath("."))
    else:
        base_path = Path(base_dir)
    return str(base_path / relative_path)


def main_window_title(editor_version: object, game_version: object = DEFAULT_GAME_VERSION) -> str:
    resolved_game_version = DEFAULT_GAME_VERSION if game_version is None else game_version
    return f"杂交版多功能修改器  {editor_version}      游戏版本：{resolved_game_version}"


def detect_game_version(window_title: str) -> Optional[float]:
    for marker, version in GAME_VERSION_MARKERS:
        if marker in window_title:
            return version
    return None


def find_running_game_process(
    *,
    find_window: Callable[[str, object | None], int],
    get_window_thread_process_id: Callable[[int], tuple[int, int]],
    get_window_text: Callable[[int], str],
    create_memory: Callable[[int], Any],
    get_process_name: Callable[[int], str],
) -> RunningGameProcess:
    hwnd = find_window("MainWindow", None)
    if not hwnd:
        raise GameProcessNotFound("PVZ Hybrid game window not found")

    _thread_id, process_id = get_window_thread_process_id(hwnd)
    window_title = get_window_text(hwnd)
    return RunningGameProcess(
        process_id=process_id,
        window_title=window_title,
        detected_version=detect_game_version(window_title),
        memory=create_memory(process_id),
        process_name=get_process_name(process_id),
    )


def evaluate_update_response(*, current_version: str, response_text: str) -> UpdateDecision:
    latest_version = response_text.strip()
    is_blocked = latest_version == BLOCKED_UPDATE_RESPONSE
    return UpdateDecision(
        latest_version=latest_version,
        is_blocked=is_blocked,
        should_open_update_window=(
            False
            if is_blocked
            else should_open_update_window(current_version, latest_version)
        ),
    )


def should_open_update_window(current_version: str, latest_version: str) -> bool:
    if latest_version == LEGACY_UPDATE_VERSION:
        return True

    current_parts = _parse_numeric_release(current_version)
    latest_parts = _parse_numeric_release(latest_version)
    if current_parts is None or latest_parts is None:
        return latest_version > current_version

    current_padded, latest_padded = _pad_release_parts(current_parts, latest_parts)
    return latest_padded > current_padded


def _parse_numeric_release(version: str) -> tuple[int, ...] | None:
    parts = version.split(".")
    if not parts or any(not part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def _pad_release_parts(
    current_parts: tuple[int, ...],
    latest_parts: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    max_length = max(len(current_parts), len(latest_parts))
    return (
        current_parts + (0,) * (max_length - len(current_parts)),
        latest_parts + (0,) * (max_length - len(latest_parts)),
    )
