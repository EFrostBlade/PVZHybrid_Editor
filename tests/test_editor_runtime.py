from pathlib import Path

import editor_runtime


def test_resource_path_uses_explicit_base_directory(tmp_path):
    assert editor_runtime.resource_path(
        "res/icon/editor.png",
        base_dir=tmp_path,
    ) == str(tmp_path / "res/icon/editor.png")


def test_resource_path_uses_pyinstaller_meipass_when_available(tmp_path):
    class FrozenRuntime:
        _MEIPASS = str(tmp_path / "bundle")

    assert editor_runtime.resource_path(
        Path("locales/en.json"),
        runtime=FrozenRuntime,
    ) == str(tmp_path / "bundle" / "locales/en.json")


def test_resource_path_falls_back_to_cwd_without_meipass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert editor_runtime.resource_path("version.txt") == str(tmp_path / "version.txt")


def test_main_window_title_formats_editor_and_game_versions():
    assert (
        editor_runtime.main_window_title("2.73", "3.17")
        == "杂交版多功能修改器  2.73      游戏版本：3.17"
    )
    assert (
        editor_runtime.main_window_title("2.73", None)
        == "杂交版多功能修改器  2.73      游戏版本：Game not found"
    )


def test_detect_game_version_matches_longest_known_window_version_first():
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v3.17}}") == 3.17
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v3.13.2}}") == 3.132
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v3.1.5}}") == 3.15
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v3.15}}") == 3.151
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v2.3.7}}") == 2.37
    assert editor_runtime.detect_game_version("PVZ Hybrid {{v2.3}}") == 2.3


def test_detect_game_version_returns_none_for_unknown_title():
    assert editor_runtime.detect_game_version("PlantsVsZombies.exe") is None


def test_find_running_game_process_returns_memory_and_detected_version():
    memory = object()
    calls = []

    def find_window(class_name, window_name):
        calls.append(("find_window", class_name, window_name))
        return 100

    def get_window_thread_process_id(hwnd):
        calls.append(("get_pid", hwnd))
        return (0, 1234)

    def get_window_text(hwnd):
        calls.append(("get_title", hwnd))
        return "PVZ Hybrid {{v3.17}}"

    def create_memory(process_id):
        calls.append(("memory", process_id))
        return memory

    def get_process_name(process_id):
        calls.append(("process_name", process_id))
        return "PVZHybrid.exe"

    process = editor_runtime.find_running_game_process(
        find_window=find_window,
        get_window_thread_process_id=get_window_thread_process_id,
        get_window_text=get_window_text,
        create_memory=create_memory,
        get_process_name=get_process_name,
    )

    assert process.process_id == 1234
    assert process.window_title == "PVZ Hybrid {{v3.17}}"
    assert process.detected_version == 3.17
    assert process.memory is memory
    assert process.process_name == "PVZHybrid.exe"
    assert calls == [
        ("find_window", "MainWindow", None),
        ("get_pid", 100),
        ("get_title", 100),
        ("memory", 1234),
        ("process_name", 1234),
    ]


def test_find_running_game_process_allows_unknown_game_version():
    process = editor_runtime.find_running_game_process(
        find_window=lambda class_name, window_name: 100,
        get_window_thread_process_id=lambda hwnd: (0, 4321),
        get_window_text=lambda hwnd: "PlantsVsZombies.exe",
        create_memory=lambda process_id: object(),
        get_process_name=lambda process_id: "PlantsVsZombies.exe",
    )

    assert process.process_id == 4321
    assert process.detected_version is None


def test_find_running_game_process_rejects_missing_window():
    try:
        editor_runtime.find_running_game_process(
            find_window=lambda class_name, window_name: 0,
            get_window_thread_process_id=lambda hwnd: (0, 0),
            get_window_text=lambda hwnd: "",
            create_memory=lambda process_id: object(),
            get_process_name=lambda process_id: "",
        )
    except editor_runtime.GameProcessNotFound as exc:
        assert str(exc) == "PVZ Hybrid game window not found"
    else:
        raise AssertionError("expected missing window to raise")


def test_evaluate_update_response_strips_response_and_detects_update():
    decision = editor_runtime.evaluate_update_response(
        current_version="2.73",
        response_text=" 2.74\n",
    )

    assert decision.latest_version == "2.74"
    assert decision.is_blocked is False
    assert decision.should_open_update_window is True


def test_evaluate_update_response_detects_blocked_version_response():
    decision = editor_runtime.evaluate_update_response(
        current_version="2.73",
        response_text="The content may contain violation information",
    )

    assert decision.latest_version == "The content may contain violation information"
    assert decision.is_blocked is True
    assert decision.should_open_update_window is False


def test_evaluate_update_response_preserves_legacy_074_update_signal():
    decision = editor_runtime.evaluate_update_response(
        current_version="2.73",
        response_text="0.74",
    )

    assert decision.should_open_update_window is True


def test_should_open_update_window_compares_numeric_release_segments():
    assert editor_runtime.should_open_update_window("2.9", "2.10") is True
    assert editor_runtime.should_open_update_window("2.9", "2.9.1") is True
    assert editor_runtime.should_open_update_window("2.9.0", "2.9") is False
    assert editor_runtime.should_open_update_window("2.10", "2.9") is False


def test_should_open_update_window_falls_back_to_existing_string_compare_for_unknown_versions():
    assert editor_runtime.should_open_update_window("beta1", "beta2") is True
    assert editor_runtime.should_open_update_window("beta2", "beta1") is False
