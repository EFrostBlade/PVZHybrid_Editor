"""Responsive Tk layout helpers for the PVZ Hybrid editor."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

DEFAULT_WINDOW_WIDTH = 900
DEFAULT_WINDOW_HEIGHT = 650
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 520
SCREEN_MARGIN = 40


class TkEvent(Protocol):
    width: int
    height: int


@dataclass(frozen=True)
class WindowGeometry:
    width: int
    height: int
    x: int
    y: int

    def as_tk_geometry(self) -> str:
        return f"{self.width}x{self.height}+{self.x}+{self.y}"

    def as_tk_size(self) -> str:
        return f"{self.width}x{self.height}"


@dataclass(frozen=True)
class ScrollableViewport:
    container: Any
    canvas: Any
    frame: Any
    vertical_scrollbar: Any
    horizontal_scrollbar: Any
    content_window_id: Any
    sync_scroll_region: Callable[[TkEvent | None], None]
    resize_content: Callable[[TkEvent], None]


def initial_window_geometry(
    *,
    screen_width: int,
    screen_height: int,
    saved_x: int | None = None,
    saved_y: int | None = None,
    target_width: int = DEFAULT_WINDOW_WIDTH,
    target_height: int = DEFAULT_WINDOW_HEIGHT,
    min_width: int = MIN_WINDOW_WIDTH,
    min_height: int = MIN_WINDOW_HEIGHT,
    screen_margin: int = SCREEN_MARGIN,
) -> WindowGeometry:
    width = _clamp(target_width, min_width, max(min_width, screen_width - screen_margin))
    height = _clamp(target_height, min_height, max(min_height, screen_height - screen_margin))
    max_x = max(0, screen_width - width)
    max_y = max(0, screen_height - height)
    default_x = max_x // 2
    default_y = (
        0 if screen_height <= height + (screen_margin * 3) else max_y // 2
    )

    x = _clamp(saved_x if saved_x is not None else default_x, 0, max_x)
    y = _clamp(saved_y if saved_y is not None else default_y, 0, max_y)
    return WindowGeometry(width=width, height=height, x=x, y=y)


def create_scrollable_viewport(
    parent: Any,
    *,
    ttk_module: Any,
    tk_module: Any,
    min_content_width: int,
    min_content_height: int,
    bottom_margin: int,
) -> ScrollableViewport:
    container = ttk_module.Frame(parent)
    container.pack(padx=5, pady=(5, bottom_margin), fill="both", expand=True)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

    canvas = tk_module.Canvas(container, highlightthickness=0)
    vertical_scrollbar = ttk_module.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview,
    )
    horizontal_scrollbar = ttk_module.Scrollbar(
        container,
        orient="horizontal",
        command=canvas.xview,
    )
    frame = ttk_module.Frame(canvas)
    content_window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    def sync_scroll_region(event: TkEvent | None = None) -> None:
        del event
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_content(event: TkEvent) -> None:
        canvas.itemconfigure(
            content_window_id,
            width=max(event.width, min_content_width),
            height=max(event.height, min_content_height),
        )

    frame.bind("<Configure>", sync_scroll_region)
    canvas.bind("<Configure>", resize_content)
    canvas.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    canvas.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    return ScrollableViewport(
        container=container,
        canvas=canvas,
        frame=frame,
        vertical_scrollbar=vertical_scrollbar,
        horizontal_scrollbar=horizontal_scrollbar,
        content_window_id=content_window_id,
        sync_scroll_region=sync_scroll_region,
        resize_content=resize_content,
    )


def _clamp(value: int, low: int, high: int) -> int:
    return min(max(value, low), high)
