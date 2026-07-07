from dataclasses import dataclass

import responsive_tk


def test_initial_window_geometry_centers_default_size_on_large_screen():
    geometry = responsive_tk.initial_window_geometry(
        screen_width=1920,
        screen_height=1080,
    )

    assert geometry.width == 900
    assert geometry.height == 650
    assert geometry.x == 510
    assert geometry.y == 215
    assert geometry.as_tk_geometry() == "900x650+510+215"


def test_initial_window_geometry_keeps_compact_windows_screen_above_taskbar_area():
    geometry = responsive_tk.initial_window_geometry(
        screen_width=1024,
        screen_height=768,
    )

    assert geometry.width == 900
    assert geometry.height == 650
    assert geometry.x == 62
    assert geometry.y == 0
    assert geometry.as_tk_geometry() == "900x650+62+0"


def test_initial_window_geometry_clamps_saved_position_to_visible_screen():
    geometry = responsive_tk.initial_window_geometry(
        screen_width=700,
        screen_height=640,
        saved_x=900,
        saved_y=-40,
    )

    assert geometry.width == 660
    assert geometry.height == 600
    assert geometry.x == 40
    assert geometry.y == 0
    assert geometry.as_tk_size() == "660x600"


def test_scrollable_viewport_keeps_design_area_available_inside_small_window():
    parent = FakeFrame()

    viewport = responsive_tk.create_scrollable_viewport(
        parent,
        ttk_module=FakeTtk,
        tk_module=FakeTk,
        min_content_width=900,
        min_content_height=650,
        bottom_margin=25,
    )

    assert viewport.container.grid_columns[0]["weight"] == 1
    assert viewport.container.grid_rows[0]["weight"] == 1
    assert viewport.canvas.options["yscrollcommand"] == viewport.vertical_scrollbar.set
    assert viewport.canvas.options["xscrollcommand"] == viewport.horizontal_scrollbar.set
    assert viewport.vertical_scrollbar.options["command"] == viewport.canvas.yview
    assert viewport.horizontal_scrollbar.options["command"] == viewport.canvas.xview

    viewport.sync_scroll_region(None)
    assert viewport.canvas.options["scrollregion"] == (0, 0, 900, 650)

    viewport.resize_content(FakeEvent(width=600, height=500))

    assert viewport.canvas.itemconfigure_calls[-1] == (
        viewport.content_window_id,
        {"width": 900, "height": 650},
    )

    viewport.resize_content(FakeEvent(width=1100, height=720))

    assert viewport.canvas.itemconfigure_calls[-1] == (
        viewport.content_window_id,
        {"width": 1100, "height": 720},
    )


@dataclass
class FakeEvent:
    width: int
    height: int


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.options = dict(kwargs)
        self.bindings = {}
        self.grid_calls = []
        self.pack_calls = []
        self.grid_columns = {}
        self.grid_rows = {}

    def configure(self, **kwargs):
        self.options.update(kwargs)

    def bind(self, event, callback):
        self.bindings[event] = callback

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def grid_columnconfigure(self, index, **kwargs):
        self.grid_columns[index] = kwargs

    def grid_rowconfigure(self, index, **kwargs):
        self.grid_rows[index] = kwargs


class FakeFrame(FakeWidget):
    pass


class FakeScrollbar(FakeWidget):
    def set(self, *args):
        self.options["set_args"] = args


class FakeCanvas(FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemconfigure_calls = []

    def create_window(self, *args, **kwargs):
        self.window_args = args
        self.window_kwargs = kwargs
        return "content-window"

    def itemconfigure(self, item_id, **kwargs):
        self.itemconfigure_calls.append((item_id, kwargs))

    def bbox(self, item_id):
        assert item_id == "all"
        return (0, 0, 900, 650)

    def yview(self, *args):
        self.options["yview_args"] = args

    def xview(self, *args):
        self.options["xview_args"] = args


class FakeTtk:
    Frame = FakeFrame
    Scrollbar = FakeScrollbar


class FakeTk:
    Canvas = FakeCanvas
