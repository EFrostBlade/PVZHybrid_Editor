"""Render and capture a Windows Tk smoke screenshot for responsive layout checks."""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol, cast

import responsive_tk

SCREENSHOT_NAME = "responsive-ui-smoke.png"
AUDIT_NAME = "responsive-ui-smoke.json"
MIN_CONTENT_WIDTH = 900
MIN_CONTENT_HEIGHT = 650
MIN_SCREENSHOT_BYTES = 100


class ImageLike(Protocol):
    def getextrema(self) -> Sequence[tuple[int, int]]:
        ...


@dataclass(frozen=True)
class SmokeAudit:
    screenshot_name: str
    screenshot_size_bytes: int
    screenshot_varies: bool
    window_width: int
    window_height: int
    canvas_width: int
    canvas_height: int
    min_content_width: int
    min_content_height: int
    scrollregion: list[int]
    horizontal_scroll_available: bool
    vertical_scroll_available: bool


def build_audit(
    *,
    screenshot_path: Path,
    screenshot_size_bytes: int,
    screenshot_varies: bool,
    window_width: int,
    window_height: int,
    canvas_width: int,
    canvas_height: int,
    scrollregion: tuple[int, int, int, int],
) -> SmokeAudit:
    scroll_width = scrollregion[2] - scrollregion[0]
    scroll_height = scrollregion[3] - scrollregion[1]
    return SmokeAudit(
        screenshot_name=screenshot_path.name,
        screenshot_size_bytes=screenshot_size_bytes,
        screenshot_varies=screenshot_varies,
        window_width=window_width,
        window_height=window_height,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        min_content_width=MIN_CONTENT_WIDTH,
        min_content_height=MIN_CONTENT_HEIGHT,
        scrollregion=list(scrollregion),
        horizontal_scroll_available=scroll_width > canvas_width,
        vertical_scroll_available=scroll_height > canvas_height,
    )


def write_audit(path: Path, audit: SmokeAudit) -> None:
    path.write_text(
        json.dumps(asdict(audit), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def assert_screenshot_evidence(path: Path, *, screenshot_varies: bool) -> None:
    if not path.exists():
        raise FileNotFoundError(f"responsive UI screenshot missing: {path}")
    if path.stat().st_size < MIN_SCREENSHOT_BYTES:
        raise ValueError(f"responsive UI screenshot too small: {path}")
    if not screenshot_varies:
        raise ValueError("responsive UI smoke captured a blank screenshot")


def run_smoke(output_dir: Path) -> SmokeAudit:  # pragma: no cover - Windows GUI smoke
    import tkinter as tk
    from tkinter import ttk

    from PIL import ImageGrab  # type: ignore[import-not-found]

    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / SCREENSHOT_NAME
    audit_path = output_dir / AUDIT_NAME

    root = tk.Tk()
    try:
        root.title("PVZ Hybrid responsive UI smoke")
        geometry = responsive_tk.initial_window_geometry(
            screen_width=root.winfo_screenwidth(),
            screen_height=root.winfo_screenheight(),
        )
        root.geometry(geometry.as_tk_geometry())
        root.minsize(responsive_tk.MIN_WINDOW_WIDTH, responsive_tk.MIN_WINDOW_HEIGHT)

        viewport = responsive_tk.create_scrollable_viewport(
            root,
            ttk_module=ttk,
            tk_module=tk,
            min_content_width=MIN_CONTENT_WIDTH,
            min_content_height=MIN_CONTENT_HEIGHT,
            bottom_margin=25,
        )
        _populate_smoke_content(viewport.frame, ttk_module=ttk)

        root.update_idletasks()
        viewport.sync_scroll_region(None)
        root.lift()
        root.attributes("-topmost", True)
        root.update()
        time.sleep(0.5)
        root.attributes("-topmost", False)
        root.update()

        left = root.winfo_rootx()
        top = root.winfo_rooty()
        right = left + root.winfo_width()
        bottom = top + root.winfo_height()
        image = ImageGrab.grab(bbox=(left, top, right, bottom)).convert("RGB")
        screenshot_varies = _image_has_pixel_variation(image)
        image.save(screenshot_path)

        scrollregion = _parse_scrollregion(viewport.canvas.cget("scrollregion"))
        audit = build_audit(
            screenshot_path=screenshot_path,
            screenshot_size_bytes=screenshot_path.stat().st_size,
            screenshot_varies=screenshot_varies,
            window_width=root.winfo_width(),
            window_height=root.winfo_height(),
            canvas_width=viewport.canvas.winfo_width(),
            canvas_height=viewport.canvas.winfo_height(),
            scrollregion=scrollregion,
        )
        assert_screenshot_evidence(screenshot_path, screenshot_varies=screenshot_varies)
        write_audit(audit_path, audit)
        return audit
    finally:
        root.destroy()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    run_smoke(args.output_dir)
    return 0


def _populate_smoke_content(parent: object, *, ttk_module: Any) -> None:  # pragma: no cover
    notebook = ttk_module.Notebook(parent)
    notebook.pack(fill="both", expand=True)

    page = ttk_module.Frame(notebook, width=MIN_CONTENT_WIDTH, height=MIN_CONTENT_HEIGHT)
    page.pack_propagate(False)
    notebook.add(page, text="Common")

    ttk_module.Label(page, text="Resource edits").place(x=8, y=8)
    for index in range(12):
        y = 36 + index * 32
        ttk_module.Label(page, text=f"Shortcut {index + 1}").place(x=220, y=y)
        ttk_module.Entry(page, width=16).place(x=320, y=y)
        ttk_module.Button(page, text="Revise", width=8).place(x=470, y=y - 3)
        ttk_module.Button(page, text=f"Action {index + 1}", width=14).place(x=735, y=y - 3)

    ttk_module.Label(page, text="Quick planting").place(x=8, y=515)
    for index in range(8):
        x = 68 + index * 98
        ttk_module.Combobox(page, width=7, values=("0", "1", "2")).place(x=x, y=542)

    ttk_module.Label(page, text="Run in background").place(x=8, y=615)
    ttk_module.Button(page, text="Load plugin").place(x=120, y=610)
    ttk_module.Label(page, text="Language").place(x=700, y=615)
    ttk_module.Combobox(page, width=10, values=("English", "中文")).place(x=770, y=610)


def _image_has_pixel_variation(image: ImageLike) -> bool:  # pragma: no cover
    extrema = image.getextrema()
    return any(channel_min != channel_max for channel_min, channel_max in extrema)


def _parse_scrollregion(value: object) -> tuple[int, int, int, int]:  # pragma: no cover
    if isinstance(value, tuple):
        if len(value) != 4:
            raise ValueError(f"unexpected canvas scrollregion: {value}")
        return cast(tuple[int, int, int, int], tuple(int(part) for part in value))
    parts = str(value).split()
    if len(parts) != 4:
        raise ValueError(f"unexpected canvas scrollregion: {value}")
    return cast(tuple[int, int, int, int], tuple(int(float(part)) for part in parts))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
