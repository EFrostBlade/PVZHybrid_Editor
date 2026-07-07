"""Static layout checks for the Windows-only editor module."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MainWindowLayout:
    imports_responsive_tk: bool
    sets_minimum_window_size: bool
    uses_initial_window_geometry: bool
    uses_scrollable_viewport: bool
    uses_bottom_bar: bool
    notebook_parent: str | None
    bottom_control_parents: dict[str, str | None]
    bottom_control_geometry_managers: dict[str, list[str]]
    literal_geometries: set[str]


@dataclass(frozen=True)
class GameDetectionAudit:
    detect_game_version_calls: int
    find_running_game_process_calls: int
    legacy_window_name_version_checks: set[str]
    legacy_win32_window_text_version_checks: set[str]


@dataclass(frozen=True)
class StartupGameSearchAudit:
    calls_update_game_on_failure: bool
    sets_not_found_status_on_failure: bool


def inspect_main_window_layout(path: Path) -> MainWindowLayout:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    visitor = _LayoutVisitor()
    visitor.visit(tree)
    return MainWindowLayout(
        imports_responsive_tk=visitor.imports_responsive_tk,
        sets_minimum_window_size=visitor.sets_minimum_window_size,
        uses_initial_window_geometry=visitor.uses_initial_window_geometry,
        uses_scrollable_viewport=visitor.uses_scrollable_viewport,
        uses_bottom_bar=visitor.uses_bottom_bar,
        notebook_parent=visitor.notebook_parent,
        bottom_control_parents=visitor.bottom_control_parents,
        bottom_control_geometry_managers={
            name: sorted(managers)
            for name, managers in visitor.bottom_control_geometry_managers.items()
        },
        literal_geometries=visitor.literal_geometries,
    )


def inspect_game_detection(path: Path) -> GameDetectionAudit:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    visitor = _GameDetectionVisitor()
    visitor.visit(tree)
    return GameDetectionAudit(
        detect_game_version_calls=visitor.detect_game_version_calls,
        find_running_game_process_calls=visitor.find_running_game_process_calls,
        legacy_window_name_version_checks=visitor.legacy_window_name_version_checks,
        legacy_win32_window_text_version_checks=visitor.legacy_win32_window_text_version_checks,
    )


def inspect_startup_game_search(path: Path) -> StartupGameSearchAudit:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    visitor = _StartupGameSearchVisitor()
    visitor.visit(tree)
    return StartupGameSearchAudit(
        calls_update_game_on_failure=visitor.calls_update_game_on_failure,
        sets_not_found_status_on_failure=visitor.sets_not_found_status_on_failure,
    )


class _LayoutVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports_responsive_tk = False
        self.sets_minimum_window_size = False
        self.uses_initial_window_geometry = False
        self.uses_scrollable_viewport = False
        self.uses_bottom_bar = False
        self.notebook_parent: str | None = None
        self.bottom_control_parents: dict[str, str | None] = {}
        self.bottom_control_geometry_managers: dict[str, set[str]] = {}
        self.literal_geometries: set[str] = set()
        self._inside_main_window = False

    def visit_Import(self, node: ast.Import) -> None:
        if any(alias.name == "responsive_tk" for alias in node.names):
            self.imports_responsive_tk = True
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "mainWindow" or self._inside_main_window:
            was_inside_main_window = self._inside_main_window
            self._inside_main_window = True
            self.generic_visit(node)
            self._inside_main_window = was_inside_main_window

    def visit_Call(self, node: ast.Call) -> None:
        call_name = _call_name(node.func)
        if call_name == "main_window.minsize":
            self.sets_minimum_window_size = True
        elif call_name == "responsive_tk.initial_window_geometry":
            self.uses_initial_window_geometry = True
        elif call_name == "responsive_tk.create_scrollable_viewport":
            self.uses_scrollable_viewport = True
        elif call_name == "main_window.geometry":
            self._collect_literal_geometry(node)
        elif call_name is not None:
            self._collect_bottom_control_geometry_manager(call_name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self._collect_bottom_control_parent(node)
        if _assigns_name(node, "page_tab") and isinstance(node.value, ast.Call):
            call_name = _call_name(node.value.func)
            if call_name == "ttk.Notebook" and node.value.args:
                self.notebook_parent = _call_name(node.value.args[0])
        self.generic_visit(node)

    def _collect_literal_geometry(self, node: ast.Call) -> None:
        first_arg = node.args[0] if node.args else None
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            self.literal_geometries.add(first_arg.value)

    def _collect_bottom_control_parent(self, node: ast.Assign) -> None:
        if not self._inside_main_window or not isinstance(node.value, ast.Call):
            return
        for name in _assigned_names(node):
            if name == "bottom_bar":
                self.uses_bottom_bar = True
            if name not in _BOTTOM_CONTROLS:
                continue
            parent = _call_name(node.value.args[0]) if node.value.args else None
            self.bottom_control_parents[name] = parent

    def _collect_bottom_control_geometry_manager(self, call_name: str) -> None:
        if not self._inside_main_window:
            return
        for control_name in _BOTTOM_CONTROLS:
            prefix = f"{control_name}."
            if not call_name.startswith(prefix):
                continue
            manager = call_name.removeprefix(prefix)
            if manager not in {"pack", "place", "grid"}:
                continue
            self.bottom_control_geometry_managers.setdefault(control_name, set()).add(manager)


class _GameDetectionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.detect_game_version_calls = 0
        self.find_running_game_process_calls = 0
        self.legacy_window_name_version_checks: set[str] = set()
        self.legacy_win32_window_text_version_checks: set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        call_name = _call_name(node.func)
        if call_name == "editor_runtime.detect_game_version":
            self.detect_game_version_calls += 1
        elif call_name == "editor_runtime.find_running_game_process":
            self.find_running_game_process_calls += 1
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        marker = _version_marker(node.left)
        if marker is None:
            self.generic_visit(node)
            return

        for operator, comparator in zip(node.ops, node.comparators, strict=True):
            if not isinstance(operator, ast.In):
                continue
            comparator_name = (
                _call_name(comparator.func)
                if isinstance(comparator, ast.Call)
                else _call_name(comparator)
            )
            if comparator_name == "window_name":
                self.legacy_window_name_version_checks.add(marker)
            elif comparator_name == "win32gui.GetWindowText":
                self.legacy_win32_window_text_version_checks.add(marker)
        self.generic_visit(node)


class _StartupGameSearchVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.calls_update_game_on_failure = False
        self.sets_not_found_status_on_failure = False
        self._inside_main_window = False
        self._inside_startup_try_find_game = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "mainWindow":
            was_inside_main_window = self._inside_main_window
            self._inside_main_window = True
            self.generic_visit(node)
            self._inside_main_window = was_inside_main_window
            return

        if self._inside_main_window and node.name == "tryFindGame":
            was_inside_startup_try_find_game = self._inside_startup_try_find_game
            self._inside_startup_try_find_game = True
            self.generic_visit(node)
            self._inside_startup_try_find_game = was_inside_startup_try_find_game
            return

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if not self._inside_startup_try_find_game:
            self.generic_visit(node)
            return

        for child in ast.walk(node):
            if isinstance(child, ast.Call) and _call_name(child.func) == "updateGame":
                self.calls_update_game_on_failure = True
            if _assigns_process_label_not_found(child):
                self.sets_not_found_status_on_failure = True
        self.generic_visit(node)


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        if parent is None:
            return node.attr
        return f"{parent}.{node.attr}"
    return None


def _version_marker(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
        return None
    if node.value.startswith("v") and any(char.isdigit() for char in node.value):
        return node.value
    return None


def _assigns_name(node: ast.Assign, name: str) -> bool:
    return any(isinstance(target, ast.Name) and target.id == name for target in node.targets)


def _assigned_names(node: ast.Assign) -> set[str]:
    return {target.id for target in node.targets if isinstance(target, ast.Name)}


def _assigns_process_label_not_found(node: ast.AST) -> bool:
    if not isinstance(node, ast.Assign):
        return False
    if not isinstance(node.value, ast.Constant) or node.value.value != "未找到游戏":
        return False
    return any(
        isinstance(target, ast.Subscript) and _call_name(target.value) == "process_label"
        for target in node.targets
    )


_BOTTOM_CONTROLS = frozenset(
    {
        "process_frame",
        "back_ground_check",
        "plugin_button",
        "unsupported_label",
        "language_frame",
    }
)
