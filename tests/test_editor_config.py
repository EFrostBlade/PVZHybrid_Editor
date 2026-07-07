import json

import pytest

import editor_config
import i18n


def test_app_config_path_and_config_file_path_use_appdata_root(tmp_path):
    app_path = editor_config.app_config_path(tmp_path)

    assert app_path == tmp_path / "PVZHybrid_Editor"
    assert editor_config.config_file_path(tmp_path) == app_path / "config.json"


def test_app_config_path_rejects_missing_appdata_root():
    with pytest.raises(RuntimeError, match="APPDATA"):
        editor_config.app_config_path(None)


def test_default_config_returns_independent_shortcut_copy():
    first = editor_config.default_config()
    second = editor_config.default_config()

    first["shortcuts"]["key1"]["key"] = "changed"

    assert second["language"] == i18n.DEFAULT_LANGUAGE
    assert second["shortcuts"]["key1"] == {"key": "ctrl+space", "action": 0}
    assert len(second["shortcuts"]) == 12


def test_load_config_returns_default_for_missing_or_invalid_json(tmp_path):
    config_path = tmp_path / "config.json"

    assert editor_config.load_config(config_path)["language"] == i18n.DEFAULT_LANGUAGE

    config_path.write_text("{not json", encoding="utf-8")

    assert editor_config.load_config(config_path)["shortcuts"]["key12"]["action"] == 11

    config_path.write_text("[]", encoding="utf-8")

    assert editor_config.load_config(config_path)["language"] == i18n.DEFAULT_LANGUAGE


def test_save_create_and_modify_config_round_trip(tmp_path):
    config_path = tmp_path / "nested" / "config.json"

    editor_config.create_config(config_path)
    config = editor_config.load_config(config_path)

    assert config["language"] == i18n.DEFAULT_LANGUAGE

    editor_config.modify_config(config_path, "data", "sunadd", 25)

    assert json.loads(config_path.read_text(encoding="utf-8"))["data"]["sunadd"] == 25

    editor_config.modify_config(config_path, "data", "sunadd", 50)

    assert json.loads(config_path.read_text(encoding="utf-8"))["data"]["sunadd"] == 50


def test_language_config_helpers_normalize_and_persist_language(tmp_path):
    config_path = tmp_path / "config.json"

    editor_config.set_config_language(config_path, "en-us")

    assert editor_config.get_config_language(config_path) == "en"

    editor_config.save_config({"language": "missing"}, config_path)

    assert editor_config.get_config_language(config_path) == i18n.DEFAULT_LANGUAGE


def test_shortcut_helpers_update_existing_config_and_create_missing_section(tmp_path):
    config_path = tmp_path / "config.json"

    assert editor_config.get_shortcuts(config_path)["key1"]["key"] == "ctrl+space"

    old_key = editor_config.set_shortcut(
        config_path,
        "key1",
        key="Ctrl+Shift+A",
        action=4,
    )

    assert old_key == "ctrl+space"
    assert editor_config.get_shortcuts(config_path)["key1"] == {
        "key": "Ctrl+Shift+A",
        "action": 4,
    }

    editor_config.save_config({}, config_path)
    old_key = editor_config.set_shortcut(
        config_path,
        "new",
        key="Ctrl+Alt+N",
        action=8,
    )

    assert old_key is None
    assert editor_config.get_shortcuts(config_path)["new"] == {"key": "Ctrl+Alt+N", "action": 8}

    editor_config.save_config({"shortcuts": []}, config_path)

    assert editor_config.get_shortcuts(config_path) == {}
