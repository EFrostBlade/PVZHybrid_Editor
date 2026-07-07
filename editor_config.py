"""Typed configuration helpers for the PVZ Hybrid editor."""
# ruff: noqa: UP007,UP045

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Optional, Union, cast

import i18n

APP_NAME = "PVZHybrid_Editor"
Config = dict[str, Any]
PathInput = Union[str, Path]

_DEFAULT_CONFIG: Config = {
    "language": i18n.DEFAULT_LANGUAGE,
    "shortcuts": {
        "key1": {"key": "ctrl+space", "action": 0},
        "key2": {"key": "Ctrl+f2", "action": 1},
        "key3": {"key": "Ctrl+f3", "action": 2},
        "key4": {"key": "Ctrl+f4", "action": 3},
        "key5": {"key": "Ctrl+f5", "action": 4},
        "key6": {"key": "Ctrl+f6", "action": 5},
        "key7": {"key": "Ctrl+f7", "action": 6},
        "key8": {"key": "Ctrl+f8", "action": 7},
        "key9": {"key": "Ctrl+f9", "action": 8},
        "key10": {"key": "Ctrl+f10", "action": 9},
        "key11": {"key": "Ctrl+f11", "action": 10},
        "key12": {"key": "Ctrl+f12", "action": 11},
    },
}


def default_config() -> Config:
    return copy.deepcopy(_DEFAULT_CONFIG)


def app_config_path(appdata_root: Optional[PathInput], app_name: str = APP_NAME) -> Path:
    if appdata_root is None:
        raise RuntimeError("APPDATA is required for PVZHybrid_Editor config")
    return Path(appdata_root) / app_name


def config_file_path(appdata_root: Optional[PathInput], app_name: str = APP_NAME) -> Path:
    return app_config_path(appdata_root, app_name=app_name) / "config.json"


def create_config(path: PathInput, config: Optional[Config] = None) -> None:
    save_config(default_config() if config is None else config, path)


def load_config(path: PathInput) -> Config:
    try:
        with Path(path).open(encoding="utf-8") as file:
            payload = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_config()
    if not isinstance(payload, dict):
        return default_config()
    return cast(Config, payload)


def save_config(config: Config, path: PathInput) -> None:
    config_path = Path(path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def modify_config(path: PathInput, section: str, key: str, value: Any) -> None:
    config = load_config(path)
    section_value = config.get(section)
    if not isinstance(section_value, dict):
        section_value = {}
        config[section] = section_value
    section_value[key] = value
    save_config(config, path)


def get_config_language(path: PathInput) -> str:
    language = load_config(path).get("language")
    return i18n.safe_language(language if isinstance(language, str) else None)


def set_config_language(path: PathInput, language: str) -> None:
    config = load_config(path)
    config["language"] = i18n.normalize_language(language)
    save_config(config, path)


def get_shortcuts(path: PathInput) -> Config:
    shortcuts = load_config(path).get("shortcuts", {})
    if isinstance(shortcuts, dict):
        return cast(Config, shortcuts)
    return {}


def set_shortcut(path: PathInput, shortcut_id: str, *, key: str, action: int) -> Optional[str]:
    config = load_config(path)
    shortcuts = config.get("shortcuts")
    if not isinstance(shortcuts, dict):
        shortcuts = {}
        config["shortcuts"] = shortcuts

    old_shortcut = shortcuts.get(shortcut_id)
    old_key = old_shortcut.get("key") if isinstance(old_shortcut, dict) else None
    shortcuts[shortcut_id] = {"key": key, "action": action}
    save_config(config, path)
    return old_key if isinstance(old_key, str) else None
