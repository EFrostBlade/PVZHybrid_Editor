from pathlib import Path

import editor_layout_audit

REPO_ROOT = Path(__file__).resolve().parents[1]
EDITOR = REPO_ROOT / "editor.py"


def test_main_window_uses_responsive_scrollable_viewport():
    layout = editor_layout_audit.inspect_main_window_layout(EDITOR)

    assert layout.imports_responsive_tk is True
    assert layout.sets_minimum_window_size is True
    assert layout.uses_initial_window_geometry is True
    assert layout.uses_scrollable_viewport is True
    assert layout.notebook_parent == "main_viewport.frame"
    assert "600x650" not in layout.literal_geometries


def test_main_window_uses_bottom_bar_instead_of_overlaying_bottom_controls():
    layout = editor_layout_audit.inspect_main_window_layout(EDITOR)

    assert layout.uses_bottom_bar is True
    assert layout.bottom_control_parents == {
        "process_frame": "bottom_bar",
        "back_ground_check": "bottom_bar",
        "plugin_button": "bottom_bar",
        "unsupported_label": "bottom_bar",
        "language_frame": "bottom_bar",
    }
    assert layout.bottom_control_geometry_managers == {
        "process_frame": ["pack"],
        "back_ground_check": ["pack"],
        "plugin_button": ["pack"],
        "unsupported_label": ["pack"],
        "language_frame": ["pack"],
    }


def test_layout_audit_reports_fixed_geometry_and_direct_notebook_parent(tmp_path):
    editor = tmp_path / "editor.py"
    editor.write_text(
        "\n".join(
            [
                "def unrelated():",
                "    main_window.geometry('300x300')",
                "",
                "def mainWindow():",
                "    main_window.geometry('600x650')",
                "    page_tab = ttk.Notebook(main_window)",
                "    process_frame = ttk.Frame(main_window)",
                "    process_frame.place(x=0, y=0)",
            ]
        ),
        encoding="utf-8",
    )

    layout = editor_layout_audit.inspect_main_window_layout(editor)

    assert layout.imports_responsive_tk is False
    assert layout.sets_minimum_window_size is False
    assert layout.uses_initial_window_geometry is False
    assert layout.uses_scrollable_viewport is False
    assert layout.uses_bottom_bar is False
    assert layout.notebook_parent == "main_window"
    assert layout.bottom_control_parents == {"process_frame": "main_window"}
    assert layout.bottom_control_geometry_managers == {"process_frame": ["place"]}
    assert layout.literal_geometries == {"600x650"}


def test_layout_audit_tolerates_dynamic_geometry_and_unparented_notebook(tmp_path):
    editor = tmp_path / "editor.py"
    editor.write_text(
        "\n".join(
            [
                "def mainWindow():",
                "    (lambda: None)()",
                "    main_window.geometry(123)",
                "    main_window.geometry()",
                "    page_tab = ttk.Notebook()",
            ]
        ),
        encoding="utf-8",
    )

    layout = editor_layout_audit.inspect_main_window_layout(editor)

    assert layout.notebook_parent is None
    assert layout.literal_geometries == set()


def test_game_detection_uses_runtime_helper_instead_of_repeated_version_chain():
    detection = editor_layout_audit.inspect_game_detection(EDITOR)

    assert detection.find_running_game_process_calls >= 2
    assert detection.detect_game_version_calls == 1
    assert detection.legacy_window_name_version_checks == set()
    assert detection.legacy_win32_window_text_version_checks == set()


def test_startup_game_search_failure_keeps_main_window_visible():
    startup_search = editor_layout_audit.inspect_startup_game_search(EDITOR)

    assert startup_search.calls_update_game_on_failure is False
    assert startup_search.sets_not_found_status_on_failure is True


def test_game_detection_audit_reports_legacy_literal_checks(tmp_path):
    editor = tmp_path / "editor.py"
    editor.write_text(
        "\n".join(
            [
                "def chooseGame():",
                "    if 'v2.0' in window_name:",
                "        pass",
                "    if 'v3.17' in win32gui.GetWindowText(hwnd):",
                "        pass",
                "    if 'v4.0' == window_name:",
                "        pass",
                "    if 'v5.0' in other_name in window_name:",
                "        pass",
                "    editor_runtime.detect_game_version(window_name)",
            ]
        ),
        encoding="utf-8",
    )

    detection = editor_layout_audit.inspect_game_detection(editor)

    assert detection.detect_game_version_calls == 1
    assert detection.find_running_game_process_calls == 0
    assert detection.legacy_window_name_version_checks == {"v2.0", "v5.0"}
    assert detection.legacy_win32_window_text_version_checks == {"v3.17"}


def test_startup_game_search_audit_reports_blocking_failure_path(tmp_path):
    editor = tmp_path / "editor.py"
    editor.write_text(
        "\n".join(
            [
                "def mainWindow():",
                "    def updateGame():",
                "        pass",
                "    def tryFindGame():",
                "        try:",
                "            pass",
                "        except:",
                "            updateGame()",
                "            process_label['text'] = '其他状态'",
            ]
        ),
        encoding="utf-8",
    )

    startup_search = editor_layout_audit.inspect_startup_game_search(editor)

    assert startup_search.calls_update_game_on_failure is True
    assert startup_search.sets_not_found_status_on_failure is False
