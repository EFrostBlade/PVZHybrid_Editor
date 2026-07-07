import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

import editor_ui_smoke


def test_build_editor_audit_records_actual_window_evidence():
    audit = editor_ui_smoke.build_editor_audit(
        screenshot_path=Path("editor-ui-smoke.png"),
        screenshot_size_bytes=4096,
        screenshot_varies=True,
        window_width=900,
        window_height=720,
        notebook_width=873,
        notebook_height=640,
        title="PVZ Hybrid",
        scrollbar_count=2,
    )

    assert audit.screenshot_name == "editor-ui-smoke.png"
    assert audit.screenshot_size_bytes == 4096
    assert audit.screenshot_varies is True
    assert audit.window_width == 900
    assert audit.window_height == 720
    assert audit.notebook_width == 873
    assert audit.notebook_height == 640
    assert audit.title == "PVZ Hybrid"
    assert audit.scrollbar_count == 2
    assert audit.scrollbars_available is True


def test_write_editor_audit_json_uses_stable_keys(tmp_path):
    audit = editor_ui_smoke.EditorSmokeAudit(
        screenshot_name="editor-ui-smoke.png",
        screenshot_size_bytes=4096,
        screenshot_varies=True,
        window_width=900,
        window_height=720,
        notebook_width=873,
        notebook_height=640,
        title="PVZ Hybrid",
        scrollbar_count=2,
        scrollbars_available=True,
    )
    output = tmp_path / "audit.json"

    editor_ui_smoke.write_audit(output, audit)

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "screenshot_name": "editor-ui-smoke.png",
        "screenshot_size_bytes": 4096,
        "screenshot_varies": True,
        "window_width": 900,
        "window_height": 720,
        "notebook_width": 873,
        "notebook_height": 640,
        "title": "PVZ Hybrid",
        "scrollbar_count": 2,
        "scrollbars_available": True,
    }


def test_assert_editor_screenshot_evidence_rejects_bad_captures(tmp_path):
    screenshot = tmp_path / "editor-ui-smoke.png"

    with pytest.raises(FileNotFoundError):
        editor_ui_smoke.assert_editor_screenshot_evidence(screenshot, screenshot_varies=True)

    screenshot.write_bytes(b"x")
    with pytest.raises(ValueError, match="too small"):
        editor_ui_smoke.assert_editor_screenshot_evidence(screenshot, screenshot_varies=True)

    screenshot.write_bytes(b"x" * 200)
    with pytest.raises(ValueError, match="blank screenshot"):
        editor_ui_smoke.assert_editor_screenshot_evidence(screenshot, screenshot_varies=False)

    editor_ui_smoke.assert_editor_screenshot_evidence(screenshot, screenshot_varies=True)


def test_find_first_widget_by_class_searches_descendants():
    notebook = FakeWidget("TNotebook")
    root = FakeWidget("Tk", children=[FakeWidget("Frame"), FakeWidget("Frame", [notebook])])

    assert editor_ui_smoke.find_first_widget_by_class(root, "TNotebook") is notebook
    assert editor_ui_smoke.find_first_widget_by_class(root, "Canvas") is None


def test_count_widgets_by_class_searches_descendants():
    root = FakeWidget(
        "Tk",
        children=[
            FakeWidget("TScrollbar"),
            FakeWidget("Frame", [FakeWidget("TScrollbar"), FakeWidget("TNotebook")]),
        ],
    )

    assert editor_ui_smoke.count_widgets_by_class(root, "TScrollbar") == 2
    assert editor_ui_smoke.count_widgets_by_class(root, "TNotebook") == 1


def test_main_runs_editor_smoke_with_output_dir(monkeypatch, tmp_path):
    captured = {}

    def fake_run_editor_smoke(output_dir):
        captured["output_dir"] = output_dir
        return editor_ui_smoke.EditorSmokeAudit(
            screenshot_name="editor-ui-smoke.png",
            screenshot_size_bytes=4096,
            screenshot_varies=True,
            window_width=900,
            window_height=720,
            notebook_width=873,
            notebook_height=640,
            title="PVZ Hybrid",
            scrollbar_count=2,
            scrollbars_available=True,
        )

    monkeypatch.setattr(editor_ui_smoke, "run_editor_smoke", fake_run_editor_smoke)

    assert editor_ui_smoke.main(["--output-dir", str(tmp_path)]) == 0
    assert captured == {"output_dir": tmp_path}


def test_main_requires_output_dir():
    with pytest.raises(SystemExit):
        editor_ui_smoke.main([])


def test_run_editor_smoke_wraps_window_factory(monkeypatch, tmp_path):
    window = FakeEditorWindow()
    updated_versions = []
    updated_memories = []

    def original_factory():
        return window

    pvz_data = SimpleNamespace(PVZ_version="2.73")

    def update_pvz_version(version):
        updated_versions.append(version)
        pvz_data.PVZ_version = version

    pvz_data.update_PVZ_version = update_pvz_version

    def update_pvz_memory(memory):
        updated_memories.append(memory)
        pvz_data.PVZ_memory = memory

    pvz_data.update_PVZ_memory = update_pvz_memory
    editor_module = SimpleNamespace(
        current_version="0.73",
        PVZ_data=pvz_data,
        requests=SimpleNamespace(),
        Messagebox=SimpleNamespace(),
        keyboard=SimpleNamespace(),
        pvz=SimpleNamespace(),
        ttk=SimpleNamespace(Window=original_factory),
        win32gui=SimpleNamespace(),
        win32process=SimpleNamespace(),
        psutil=SimpleNamespace(),
    )

    def main_window():
        hwnd = editor_module.win32gui.FindWindow("MainWindow", None)
        _, process_id = editor_module.win32process.GetWindowThreadProcessId(hwnd)
        editor_module.PVZ_data.update_PVZ_memory(editor_module.Pymem(process_id))

        assert isinstance(editor_module.PVZ_data.PVZ_version, (int, float))
        assert editor_module.PVZ_data.PVZ_memory.read_uint(0x41C965) == 304
        assert editor_module.PVZ_data.PVZ_memory.process_id == 1234
        created_window = editor_module.ttk.Window()
        created_window.title("PVZ Hybrid")
        created_window.mainloop()

    editor_module.mainWindow = main_window

    pil_module = ModuleType("PIL")
    pil_module.ImageGrab = SimpleNamespace(grab=lambda bbox: FakeImage(bbox))
    monkeypatch.setitem(sys.modules, "PIL", pil_module)
    monkeypatch.setattr(editor_ui_smoke.importlib, "import_module", lambda name: editor_module)
    monkeypatch.setattr(
        editor_ui_smoke.responsive_ui_smoke,
        "_image_has_pixel_variation",
        lambda image: True,
    )

    audit = editor_ui_smoke.run_editor_smoke(tmp_path)

    assert audit.screenshot_name == "editor-ui-smoke.png"
    assert audit.screenshot_size_bytes == 200
    assert audit.scrollbar_count == 2
    assert audit.scrollbars_available is True
    assert window.after_delays == [1500]
    assert window.mainloop_called is True
    assert window.destroyed is True
    assert updated_versions == [3.17]
    assert len(updated_memories) == 2
    assert editor_module.ttk.Window is original_factory


class FakeWidget:
    def __init__(self, widget_class, children=None, width=40, height=20):
        self._widget_class = widget_class
        self._children = children or []
        self._width = width
        self._height = height

    def winfo_class(self):
        return self._widget_class

    def winfo_children(self):
        return self._children

    def winfo_width(self):
        return self._width

    def winfo_height(self):
        return self._height


class FakeEditorWindow(FakeWidget):
    def __init__(self):
        super().__init__(
            "Tk",
            children=[
                FakeWidget("TNotebook", width=873, height=640),
                FakeWidget("TScrollbar"),
                FakeWidget("TScrollbar"),
            ],
            width=900,
            height=720,
        )
        self.after_delays = []
        self.after_callbacks = []
        self.mainloop_called = False
        self.destroyed = False
        self._title = ""

    def after(self, delay, callback):
        self.after_delays.append(delay)
        self.after_callbacks.append(callback)

    def mainloop(self, *args, **kwargs):
        self.mainloop_called = True
        for callback in self.after_callbacks:
            callback()

    def update_idletasks(self):
        pass

    def update(self):
        pass

    def winfo_rootx(self):
        return 10

    def winfo_rooty(self):
        return 20

    def title(self, value=None):
        if value is not None:
            self._title = value
        return self._title

    def destroy(self):
        self.destroyed = True


class FakeImage:
    def __init__(self, bbox):
        self.bbox = bbox

    def convert(self, mode):
        return self

    def save(self, path):
        Path(path).write_bytes(b"x" * 200)
