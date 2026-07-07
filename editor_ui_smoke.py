"""Launch the real editor window on Windows and capture a responsive UI screenshot."""

from __future__ import annotations

import argparse
import importlib
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import responsive_ui_smoke

SCREENSHOT_NAME = "editor-ui-smoke.png"
AUDIT_NAME = "editor-ui-smoke.json"
MIN_SCREENSHOT_BYTES = 100
SMOKE_GAME_VERSION = 3.17


@dataclass(frozen=True)
class EditorSmokeAudit:
    screenshot_name: str
    screenshot_size_bytes: int
    screenshot_varies: bool
    window_width: int
    window_height: int
    notebook_width: int
    notebook_height: int
    title: str
    scrollbar_count: int
    scrollbars_available: bool


def build_editor_audit(
    *,
    screenshot_path: Path,
    screenshot_size_bytes: int,
    screenshot_varies: bool,
    window_width: int,
    window_height: int,
    notebook_width: int,
    notebook_height: int,
    title: str,
    scrollbar_count: int,
) -> EditorSmokeAudit:
    return EditorSmokeAudit(
        screenshot_name=screenshot_path.name,
        screenshot_size_bytes=screenshot_size_bytes,
        screenshot_varies=screenshot_varies,
        window_width=window_width,
        window_height=window_height,
        notebook_width=notebook_width,
        notebook_height=notebook_height,
        title=title,
        scrollbar_count=scrollbar_count,
        scrollbars_available=scrollbar_count >= 2,
    )


def write_audit(path: Path, audit: EditorSmokeAudit) -> None:
    path.write_text(
        json.dumps(asdict(audit), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def assert_editor_screenshot_evidence(path: Path, *, screenshot_varies: bool) -> None:
    if not path.exists():
        raise FileNotFoundError(f"editor UI screenshot missing: {path}")
    if path.stat().st_size < MIN_SCREENSHOT_BYTES:
        raise ValueError(f"editor UI screenshot too small: {path}")
    if not screenshot_varies:
        raise ValueError("editor UI smoke captured a blank screenshot")


def find_first_widget_by_class(widget: Any, widget_class: str) -> Any | None:
    if widget.winfo_class() == widget_class:
        return widget
    for child in widget.winfo_children():
        found = find_first_widget_by_class(child, widget_class)
        if found is not None:
            return found
    return None


def count_widgets_by_class(widget: Any, widget_class: str) -> int:
    count = 1 if widget.winfo_class() == widget_class else 0
    for child in widget.winfo_children():
        count += count_widgets_by_class(child, widget_class)
    return count


def run_editor_smoke(output_dir: Path) -> EditorSmokeAudit:  # pragma: no cover - Windows GUI
    from PIL import ImageGrab  # type: ignore[import-not-found]

    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / SCREENSHOT_NAME
    audit_path = output_dir / AUDIT_NAME
    captured: dict[str, EditorSmokeAudit] = {}

    editor_module = importlib.import_module("editor")

    _patch_editor_runtime(editor_module)
    original_window_factory = editor_module.ttk.Window

    def smoke_window_factory(*args: object, **kwargs: object) -> Any:
        window = original_window_factory(*args, **kwargs)
        original_mainloop = window.mainloop

        def smoke_mainloop(*mainloop_args: object, **mainloop_kwargs: object) -> object:
            window.after(1500, lambda: _capture_and_close(window))
            return original_mainloop(*mainloop_args, **mainloop_kwargs)

        window.mainloop = smoke_mainloop
        return window

    def _capture_and_close(window: Any) -> None:
        window.update_idletasks()
        window.update()

        left = window.winfo_rootx()
        top = window.winfo_rooty()
        right = left + window.winfo_width()
        bottom = top + window.winfo_height()
        image = ImageGrab.grab(bbox=(left, top, right, bottom)).convert("RGB")
        screenshot_varies = responsive_ui_smoke._image_has_pixel_variation(image)
        image.save(screenshot_path)

        notebook = find_first_widget_by_class(window, "TNotebook")
        scrollbar_count = count_widgets_by_class(window, "TScrollbar")
        audit = build_editor_audit(
            screenshot_path=screenshot_path,
            screenshot_size_bytes=screenshot_path.stat().st_size,
            screenshot_varies=screenshot_varies,
            window_width=window.winfo_width(),
            window_height=window.winfo_height(),
            notebook_width=notebook.winfo_width() if notebook is not None else 0,
            notebook_height=notebook.winfo_height() if notebook is not None else 0,
            title=window.title(),
            scrollbar_count=scrollbar_count,
        )
        assert_editor_screenshot_evidence(screenshot_path, screenshot_varies=screenshot_varies)
        write_audit(audit_path, audit)
        captured["audit"] = audit
        window.destroy()

    editor_module.ttk.Window = smoke_window_factory
    try:
        editor_module.mainWindow()
    finally:
        editor_module.ttk.Window = original_window_factory

    return captured["audit"]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    run_editor_smoke(args.output_dir)
    return 0


def _patch_editor_runtime(editor_module: Any) -> None:  # pragma: no cover - Windows GUI
    class SmokePVZMemory:
        def __init__(self, process_id: int = 1234) -> None:
            self.process_id = process_id

        def read_uint(self, address: int) -> int:
            if address in {0x41C965, 0x41C905}:
                return 304
            return 0

        def read_ushort(self, address: int) -> int:
            return 0

        def read_uchar(self, address: int) -> int:
            return 0

        def read_bool(self, address: int) -> bool:
            return False

        def read_float(self, address: int) -> float:
            return 0.0

        def read_bytes(self, address: int, length: int) -> bytes:
            return b"\x00" * length

        def write_int(self, address: int, value: object) -> None:
            return None

        def write_float(self, address: int, value: object) -> None:
            return None

        def write_bool(self, address: int, value: object) -> None:
            return None

        def write_ushort(self, address: int, value: object) -> None:
            return None

        def write_uchar(self, address: int, value: object) -> None:
            return None

        def write_bytes(self, address: int, value: object, length: int | None = None) -> None:
            return None

    class SmokeProcess:
        def __init__(self, process_id: int) -> None:
            self.process_id = process_id

        def name(self) -> str:
            return "PVZHybrid.exe"

    class Response:
        text = str(editor_module.current_version)

    editor_module.PVZ_data.update_PVZ_memory(SmokePVZMemory())
    editor_module.PVZ_data.update_PVZ_version(SMOKE_GAME_VERSION)
    editor_module.Pymem = SmokePVZMemory
    editor_module.win32gui.FindWindow = lambda *args, **kwargs: 1
    editor_module.win32gui.GetWindowText = lambda *args, **kwargs: "v3.17"
    editor_module.win32process.GetWindowThreadProcessId = lambda *args, **kwargs: (0, 1234)
    editor_module.psutil.Process = SmokeProcess
    editor_module.requests.get = lambda *args, **kwargs: Response()
    editor_module.Messagebox.show_error = lambda *args, **kwargs: None
    editor_module.keyboard.add_hotkey = lambda *args, **kwargs: None
    editor_module.keyboard.remove_hotkey = lambda *args, **kwargs: None

    editor_module.pvz.getShovel = lambda: 0
    editor_module.pvz.getMap = lambda: False
    editor_module.pvz.getSun = lambda: 0
    editor_module.pvz.getSilver = lambda: 0
    editor_module.pvz.getGold = lambda: 0
    editor_module.pvz.getDiamond = lambda: 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
