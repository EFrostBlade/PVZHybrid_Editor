"""Isolated real-Tk startup probe, with no real network or game access.

Run from the repository root: python tests/gui_startup_probe.py
"""
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class ReadOnlyMemory:
    process_id = 0

    def read_uint(self, address):
        return 772 if address in (0x41C965, 0x41C905) else 0

    read_int = read_uint
    read_uchar = read_uint
    read_ushort = read_uint
    read_float = read_uint
    read_bool = read_uint

    def read_bytes(self, address, size):
        return bytes(size)


def main():
    with tempfile.TemporaryDirectory(prefix="editor-startup-") as directory:
        os.environ["APPDATA"] = directory
        import tkinter as tk
        tk_class, toplevel_class = tk.Tk, tk.Toplevel
        import editor as editor

        entered, release = threading.Event(), threading.Event()
        callback_errors = []
        metrics = {}
        owner = threading.get_ident()
        original_mainloop = tk.Misc.mainloop
        original_report = tk_class.report_callback_exception

        def fetch(*args, **kwargs):
            assert threading.get_ident() != owner
            assert kwargs["timeout"] == (2, 3)
            entered.set()
            assert release.wait(10), "UI did not release the slow update request"
            return SimpleNamespace(text="0.76", raise_for_status=lambda: None)

        def widgets(root):
            yield root
            for child in root.winfo_children():
                yield from widgets(child)

        def report(root, exc_type, value, tb):
            callback_errors.append(str(value))
            original_report(root, exc_type, value, tb)
            release.set()
            root.destroy()

        def inspect(root, *args, **kwargs):
            metrics["construction_seconds"] = time.perf_counter() - started
            assert not entered.is_set(), "update request ran before mainloop"
            all_widgets = list(widgets(root))
            combos = [w for w in all_widgets if hasattr(w, "_i18n_original_values")]
            metrics["widgets"] = len(all_widgets)
            metrics["comboboxes"] = len(combos)
            notebook = next(w for w in all_widgets
                            if hasattr(w, "tabs") and len(w.tabs()) == 9)
            editor.i18n.set_language("en")
            selection = tk.StringVar(root, value="全部")
            selected_combo = editor.ttk.Combobox(root, values=["全部"], textvariable=selection)
            assert selected_combo.current() == 0
            assert selection.get() == editor.i18n.translate("全部")
            assert selected_combo.get() == "全部"
            selected_combo.destroy()
            editor.i18n.set_language("zh_CN")

            def first_frame():
                metrics["first_frame_seconds"] = time.perf_counter() - started
                assert root.winfo_ismapped()
                assert entered.is_set(), "background update did not start"
                assert not release.is_set()
                release.set()
                root.after(100, check_update_window)

            def check_update_window(attempt=0):
                popups = [w for w in root.winfo_children()
                          if isinstance(w, toplevel_class) and w.title() == "有新版本"]
                if not popups and attempt < 20:
                    root.after(100, lambda: check_update_window(attempt + 1))
                    return
                assert len(popups) == 1, "new-version window was not shown"
                popup = popups[0]
                assert len(popup.payment_images) == 2
                root.tk.call(popup.protocol("WM_DELETE_WINDOW"))
                assert root.winfo_exists(), "closing update prompt closed the application"
                editor.set_game_version(3.18)
                editor.set_game_version(3.19)
                editor.i18n.set_language("en")
                editor.i18n.refresh_widgets(root)
                for name in ("读报伽刚特尔", "基因寒冰菇", "全息仙人掌子弹"):
                    combo = next(w for w in combos if name in w._i18n_original_values)
                    combo.current(combo._i18n_original_values.index(name))
                    assert combo.get() == name
                editor.i18n.set_language("zh_CN")
                editor.i18n.refresh_widgets(root)
                root.after(10, lambda: visit_tab(0))

            def visit_tab(index):
                notebook.select(index)
                if index < 8:
                    root.after(110, lambda: visit_tab(index + 1))
                else:
                    metrics["tabs_visited"] = 9
                    root.after(110, root.destroy)

            root.after(250, first_frame)
            original_mainloop(root, *args, **kwargs)

        game = SimpleNamespace(detected_version=3.19, memory=ReadOnlyMemory(),
                               process_id=0, process_name="startup-test")
        with patch.object(editor.editor_runtime, "find_running_game_process", return_value=game), \
             patch.object(editor.requests, "get", side_effect=fetch), \
             patch.object(editor.keyboard, "add_hotkey"), \
             patch.object(editor.Messagebox, "show_error", side_effect=AssertionError("startup error dialog")), \
             patch.object(tk_class, "report_callback_exception", report), \
             patch.object(tk.Misc, "mainloop", inspect):
            started = time.perf_counter()
            try:
                editor.mainWindow()
            finally:
                release.set()
        assert not callback_errors, callback_errors
        assert metrics.get("tabs_visited") == 9, metrics
        print("STARTUP_RESULT " + json.dumps(metrics), flush=True)


if __name__ == "__main__":
    main()
