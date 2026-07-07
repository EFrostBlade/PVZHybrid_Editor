"""Runtime i18n support for the PVZ Hybrid editor."""

from __future__ import annotations

import json
import weakref
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

DEFAULT_LANGUAGE = "zh_CN"
LANGUAGE_ORDER = ("zh_CN", "en", "es", "fr", "de", "ja", "ko", "ru")
LOCALES_DIR = Path(__file__).resolve().parent / "locales"

_ALIASES = {
    "zh": "zh_CN",
    "zh-cn": "zh_CN",
    "zh_cn": "zh_CN",
    "cn": "zh_CN",
    "en-us": "en",
    "en_us": "en",
    "es-es": "es",
    "es_es": "es",
}


@dataclass(frozen=True)
class Language:
    code: str
    language_name: str
    native_name: str


_catalog_cache: dict[str, dict[str, str]] = {}
_language_cache: list[Language] | None = None
_current_language = DEFAULT_LANGUAGE
_widgets: weakref.WeakKeyDictionary[Any, dict[str, Any]] = weakref.WeakKeyDictionary()
_notebooks: weakref.WeakKeyDictionary[Any, dict[Any, str]] = weakref.WeakKeyDictionary()
_window_titles: weakref.WeakKeyDictionary[Any, str] = weakref.WeakKeyDictionary()
_patched_modules: weakref.WeakSet[Any] = weakref.WeakSet()


def supported_languages() -> list[Language]:
    global _language_cache
    if _language_cache is not None:
        return list(_language_cache)

    languages: list[Language] = []
    for code in LANGUAGE_ORDER:
        payload = _load_locale_payload(code)
        languages.append(
            Language(
                code=payload["code"],
                language_name=payload["language_name"],
                native_name=payload["native_name"],
            )
        )
    _language_cache = languages
    return list(languages)


def language_options() -> list[str]:
    return [language.native_name for language in supported_languages()]


def language_code_for_native_name(native_name: str) -> str:
    for language in supported_languages():
        if language.native_name == native_name:
            return language.code
    raise ValueError(f"Unsupported language option: {native_name}")


def normalize_language(language: str | None) -> str:
    if not language:
        return DEFAULT_LANGUAGE
    candidate = _ALIASES.get(language.lower(), language)
    if candidate not in LANGUAGE_ORDER:
        raise ValueError(f"Unsupported language: {language}")
    return candidate


def safe_language(language: str | None) -> str:
    try:
        return normalize_language(language)
    except ValueError:
        return DEFAULT_LANGUAGE


def set_language(language: str) -> None:
    global _current_language
    _current_language = normalize_language(language)


def get_language() -> str:
    return _current_language


def translate(text: str, language: str | None = None, **kwargs: Any) -> str:
    code = normalize_language(language or _current_language)
    catalog = _load_catalog(code)
    translated = catalog.get(text)
    if translated is None:
        translated = _translate_segments(text, catalog)
    if kwargs:
        try:
            return translated.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return translated
    return translated


def translate_values(values: Iterable[Any], language: str | None = None) -> list[Any]:
    return [
        translate(value, language=language) if isinstance(value, str) else value
        for value in values
    ]


def register_widget(
    widget: Any,
    *,
    text: str | None = None,
    values: Iterable[Any] | None = None,
) -> None:
    metadata: dict[str, Any] = {}
    if isinstance(text, str):
        metadata["text"] = text
    if values is not None:
        metadata["values"] = list(values)
    if not metadata:
        return
    _widgets[widget] = metadata
    _apply_widget_translation(widget, metadata)


def register_notebook_tab(notebook: Any, tab_id: Any, text: str) -> None:
    tabs = _notebooks.setdefault(notebook, {})
    tabs[tab_id] = text
    _apply_notebook_translation(notebook, tab_id, text)


def register_window_title(window: Any, title: str) -> None:
    _window_titles[window] = title
    _apply_window_title(window, title)


def refresh_widgets(root: Any | None = None) -> None:
    del root  # Current registry is process-wide; root is reserved for future scoping.

    stale_widgets: list[Any] = []
    for widget, metadata in list(_widgets.items()):
        try:
            _apply_widget_translation(widget, metadata)
        except Exception:
            stale_widgets.append(widget)
    for widget in stale_widgets:
        _widgets.pop(widget, None)

    stale_notebooks: list[Any] = []
    for notebook, tabs in list(_notebooks.items()):
        try:
            for tab_id, text in list(tabs.items()):
                _apply_notebook_translation(notebook, tab_id, text)
        except Exception:
            stale_notebooks.append(notebook)
    for notebook in stale_notebooks:
        _notebooks.pop(notebook, None)

    stale_windows: list[Any] = []
    for window, title in list(_window_titles.items()):
        try:
            _apply_window_title(window, title)
        except Exception:
            stale_windows.append(window)
    for window in stale_windows:
        _window_titles.pop(window, None)


def install_tk_i18n(ttk_module: Any, tk_module: Any | None = None) -> None:
    for module in (ttk_module, tk_module):
        if module is None or module in _patched_modules:
            continue
        for class_name in (
            "Button",
            "Checkbutton",
            "Label",
            "Labelframe",
            "LabelFrame",
            "Menubutton",
            "Radiobutton",
            "Scale",
            "Combobox",
            "Notebook",
            "Toplevel",
            "Window",
            "Tk",
        ):
            _patch_widget_factory(module, class_name)
        _patched_modules.add(module)


def _load_locale_payload(code: str) -> dict[str, Any]:
    path = LOCALES_DIR / f"{code}.json"
    with path.open("r", encoding="utf-8") as file:
        payload = cast(dict[str, Any], json.load(file))
    if payload.get("code") != code:
        raise ValueError(f"Locale code mismatch in {path}")
    return payload


def _load_catalog(code: str) -> dict[str, str]:
    if code not in _catalog_cache:
        payload = _load_locale_payload(code)
        translations = payload.get("translations", {})
        if not isinstance(translations, dict):
            raise ValueError(f"Invalid translations for locale {code}")
        _catalog_cache[code] = {
            str(source): str(target) for source, target in translations.items()
        }
    return _catalog_cache[code]


def _translate_segments(text: str, catalog: dict[str, str]) -> str:
    translated = text
    for source, target in sorted(catalog.items(), key=lambda item: len(item[0]), reverse=True):
        if source == target or "{" in source or "}" in source:
            continue
        if source in translated:
            translated = translated.replace(source, target)
    return translated


def _apply_widget_translation(widget: Any, metadata: dict[str, Any]) -> None:
    updates: dict[str, Any] = {}
    if "text" in metadata:
        updates["text"] = translate(metadata["text"])
    if "values" in metadata:
        selected_source = _get_selected_source(widget)
        updates["values"] = translate_values(metadata["values"])
    if updates:  # pragma: no branch
        widget.configure(**updates)
    if "values" in metadata and selected_source in metadata["values"]:
        _set_selected_source(widget, selected_source)


def _apply_notebook_translation(notebook: Any, tab_id: Any, text: str) -> None:
    notebook.tab(tab_id, text=translate(text))


def _apply_window_title(window: Any, title: str) -> None:
    title_method = getattr(window, "_i18n_original_title", None)
    if title_method is None:
        title_method = window.title
    title_method(translate(title))


def _patch_widget_factory(module: Any, class_name: str) -> None:
    original = getattr(module, class_name, None)
    if original is None or getattr(original, "_i18n_wrapped", False):
        return

    def factory(*args: Any, **kwargs: Any) -> Any:
        original_text = kwargs.get("text")
        original_values = kwargs.get("values")

        if isinstance(original_text, str):
            kwargs["text"] = translate(original_text)
        if original_values is not None:
            kwargs["values"] = translate_values(original_values)

        widget = original(*args, **kwargs)
        if original_values is not None:
            _patch_value_selection_methods(widget, list(original_values))
        register_widget(
            widget,
            text=original_text if isinstance(original_text, str) else None,
            values=original_values,
        )
        if class_name == "Notebook":
            _patch_notebook_instance(widget)
        if class_name in {"Tk", "Toplevel", "Window"}:
            _patch_title_method(widget)
        return widget

    factory._i18n_wrapped = True  # type: ignore[attr-defined]
    setattr(module, class_name, factory)


def _patch_notebook_instance(notebook: Any) -> None:
    if getattr(notebook, "_i18n_notebook_patched", False):
        return
    original_add = notebook.add

    def add(child: Any, **kwargs: Any) -> Any:
        original_text = kwargs.get("text")
        if isinstance(original_text, str):
            kwargs["text"] = translate(original_text)
        result = original_add(child, **kwargs)
        if isinstance(original_text, str):
            register_notebook_tab(notebook, child, original_text)
        return result

    notebook.add = add
    notebook._i18n_notebook_patched = True


def _patch_title_method(window: Any) -> None:
    if getattr(window, "_i18n_title_patched", False) or not hasattr(window, "title"):
        return
    original_title = window.title

    def title(text: str | None = None) -> Any:
        if text is None:
            return original_title()
        if isinstance(text, str):
            register_window_title(window, text)
            return None
        return original_title(text)

    window._i18n_original_title = original_title
    window.title = title
    window._i18n_title_patched = True


def _patch_value_selection_methods(widget: Any, original_values: list[Any]) -> None:
    widget._i18n_original_values = list(original_values)
    if getattr(widget, "_i18n_value_methods_patched", False):
        return
    if not hasattr(widget, "get") or not hasattr(widget, "set"):
        return

    original_get = widget.get
    original_set = widget.set

    def get() -> Any:
        return _source_for_display(widget, original_get())

    def set_value(value: Any) -> Any:
        return original_set(_display_for_source(widget, value))

    widget._i18n_original_get = original_get
    widget._i18n_original_set = original_set
    widget.get = get
    widget.set = set_value
    widget._i18n_value_methods_patched = True


def _get_selected_source(widget: Any) -> Any:
    if not hasattr(widget, "get"):
        return None
    try:
        return widget.get()
    except Exception:
        return None


def _set_selected_source(widget: Any, source: Any) -> None:
    if not hasattr(widget, "set"):
        return
    try:
        widget.set(source)
    except Exception:
        return


def _display_for_source(widget: Any, value: Any) -> Any:
    original_values = getattr(widget, "_i18n_original_values", [])
    if isinstance(value, str) and value in original_values:
        return translate(value)
    return value


def _source_for_display(widget: Any, value: Any) -> Any:
    if not isinstance(value, str):
        return value
    for source in getattr(widget, "_i18n_original_values", []):
        if not isinstance(source, str):
            continue
        if value == source:
            return source
        for language in LANGUAGE_ORDER:
            if value == translate(source, language=language):
                return source
    return value
