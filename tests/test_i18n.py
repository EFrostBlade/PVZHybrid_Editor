import json
from pathlib import Path

import pytest

import i18n

REPO_ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = REPO_ROOT / "locales"


def test_supported_languages_include_required_eight_languages():
    codes = [language.code for language in i18n.supported_languages()]

    assert codes == ["zh_CN", "en", "es", "fr", "de", "ja", "ko", "ru"]
    assert len(codes) == 8


def test_locale_files_exist_and_share_identical_translation_keys():
    expected_codes = {language.code for language in i18n.supported_languages()}
    locale_paths = {path.stem: path for path in LOCALES_DIR.glob("*.json")}

    assert set(locale_paths) == expected_codes

    key_sets = {}
    for code, path in locale_paths.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["code"] == code
        assert payload["language_name"]
        assert payload["native_name"]
        assert payload["translations"]
        key_sets[code] = set(payload["translations"])

    assert len({frozenset(keys) for keys in key_sets.values()}) == 1


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("zh_CN", "选择游戏"),
        ("en", "Choose game"),
        ("es", "Elegir juego"),
    ],
)
def test_translate_known_ui_text(language, expected):
    assert i18n.translate("选择游戏", language=language) == expected


def test_language_helpers_normalize_aliases_and_fallbacks():
    i18n.set_language("en-us")

    assert i18n.get_language() == "en"
    assert "English" in i18n.language_options()
    assert i18n.language_code_for_native_name("English") == "en"
    assert i18n.normalize_language(None) == i18n.DEFAULT_LANGUAGE
    assert i18n.safe_language("missing") == i18n.DEFAULT_LANGUAGE

    with pytest.raises(ValueError):
        i18n.language_code_for_native_name("Missing")
    with pytest.raises(ValueError):
        i18n.normalize_language("missing")

    i18n.set_language(i18n.DEFAULT_LANGUAGE)


def test_translate_interpolates_named_values_and_falls_back_to_source_text():
    assert (
        i18n.translate(
            "app.title",
            language="en",
            version="2.73",
            game_version="3.17",
        )
        == "PVZ Hybrid Multi-tool Editor  2.73      Game version: 3.17"
    )
    assert i18n.translate("未收录文案", language="en") == "未收录文案"
    assert (
        i18n.translate("app.title", language="en", version="2.73")
        == "PVZ Hybrid Multi-tool Editor  {version}      Game version: {game_version}"
    )


def test_unsupported_language_is_rejected():
    with pytest.raises(ValueError):
        i18n.set_language("pt_BR")


class FakeWidget:
    def __init__(self):
        self.options = {}

    def configure(self, **kwargs):
        self.options.update(kwargs)


def test_registered_widgets_refresh_when_language_changes():
    widget = FakeWidget()
    i18n.set_language("zh_CN")
    i18n.register_widget(widget, text="选择游戏")

    i18n.set_language("es")
    i18n.refresh_widgets()
    assert widget.options["text"] == "Elegir juego"

    i18n.set_language("en")
    i18n.refresh_widgets()
    assert widget.options["text"] == "Choose game"


def test_register_widget_ignores_empty_metadata():
    widget = FakeWidget()

    i18n.register_widget(widget)
    widget.configure(text="manual")
    i18n.refresh_widgets()

    assert widget.options["text"] == "manual"


def test_translate_values_preserves_unknown_items():
    assert i18n.translate_values(["选择游戏", "Ctrl+F2"], language="en") == [
        "Choose game",
        "Ctrl+F2",
    ]


def test_invalid_locale_payloads_are_rejected(tmp_path, monkeypatch):
    locale_dir = tmp_path / "locales"
    locale_dir.mkdir()

    (locale_dir / "zh_CN.json").write_text(
        json.dumps(
            {
                "code": "en",
                "language_name": "Broken",
                "native_name": "Broken",
                "translations": {},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(i18n, "LOCALES_DIR", locale_dir)
    monkeypatch.setattr(i18n, "_language_cache", None)

    with pytest.raises(ValueError, match="Locale code mismatch"):
        i18n.supported_languages()


def test_invalid_catalog_translations_are_rejected(tmp_path, monkeypatch):
    locale_dir = tmp_path / "locales"
    locale_dir.mkdir()

    (locale_dir / "zh_CN.json").write_text(
        json.dumps(
            {
                "code": "zh_CN",
                "language_name": "Chinese",
                "native_name": "简体中文",
                "translations": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(i18n, "LOCALES_DIR", locale_dir)
    monkeypatch.setattr(i18n, "_catalog_cache", {})

    with pytest.raises(ValueError, match="Invalid translations"):
        i18n.translate("选择游戏", language="zh_CN")


def test_segment_translation_skips_identity_and_format_keys(tmp_path, monkeypatch):
    locale_dir = tmp_path / "locales"
    locale_dir.mkdir()
    (locale_dir / "zh_CN.json").write_text(
        json.dumps(
            {
                "code": "zh_CN",
                "language_name": "Chinese",
                "native_name": "简体中文",
                "translations": {
                    "阳光": "Sun",
                    "same": "same",
                    "Ctrl+{key}": "Ctrl+{key}",
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(i18n, "LOCALES_DIR", locale_dir)
    monkeypatch.setattr(i18n, "_catalog_cache", {})

    assert i18n.translate("阳光 same Ctrl+{key}", language="zh_CN") == "Sun same Ctrl+{key}"


def test_install_tk_i18n_translates_widgets_and_notebook_tabs():
    class FakeLabel:
        def __init__(self, *args, **kwargs):
            del args
            self.options = dict(kwargs)

        def configure(self, **kwargs):
            self.options.update(kwargs)

    class FakeNotebook:
        def __init__(self, *args, **kwargs):
            del args, kwargs
            self.tabs = {}

        def add(self, child, **kwargs):
            self.tabs[child] = kwargs

        def tab(self, child, **kwargs):
            self.tabs[child].update(kwargs)

    class FakeTtk:
        Label = FakeLabel
        Notebook = FakeNotebook

    i18n.set_language("en")
    i18n.install_tk_i18n(FakeTtk)

    label = FakeTtk.Label(text="选择游戏")
    notebook = FakeTtk.Notebook()
    notebook.add("common", text="常用功能")

    assert label.options["text"] == "Choose game"
    assert notebook.tabs["common"]["text"] == "Common tools"

    i18n.set_language("es")
    i18n.refresh_widgets()

    assert label.options["text"] == "Elegir juego"
    assert notebook.tabs["common"]["text"] == "Herramientas comunes"


def test_install_tk_i18n_patches_combobox_window_and_missing_classes():
    class FakeLabel:
        def __init__(self, *args, **kwargs):
            del args
            self.options = dict(kwargs)

        def configure(self, **kwargs):
            self.options.update(kwargs)

    class FakeCombobox:
        def __init__(self, *args, **kwargs):
            del args
            self.options = dict(kwargs)
            self.selected = ""

        def configure(self, **kwargs):
            self.options.update(kwargs)

        def get(self):
            return self.selected

        def set(self, value):
            self.selected = value

    class FakeNotebook:
        def __init__(self, *args, **kwargs):
            del args, kwargs
            self.tabs = {}

        def add(self, child, **kwargs):
            self.tabs[child] = kwargs
            return child

        def tab(self, child, **kwargs):
            self.tabs[child].update(kwargs)

    class FakeWindow:
        def __init__(self, *args, **kwargs):
            del args, kwargs
            self.current_title = "initial"

        def title(self, text=None):
            if text is None:
                return self.current_title
            self.current_title = text
            return "title-result"

    class FakeTtk:
        Label = FakeLabel
        Combobox = FakeCombobox
        Notebook = FakeNotebook
        Window = FakeWindow

    i18n.set_language("en")
    i18n.install_tk_i18n(FakeTtk)
    i18n.install_tk_i18n(FakeTtk)

    label = FakeTtk.Label(text=123)
    assert label.options["text"] == 123

    combobox = FakeTtk.Combobox(values=[1, "选择游戏"])
    assert combobox.options["values"] == [1, "Choose game"]
    combobox.set(1)
    assert combobox.get() == 1
    combobox.selected = "选择游戏"
    assert combobox.get() == "选择游戏"
    combobox.selected = "Choose game"
    assert combobox.get() == "选择游戏"
    combobox.set("Ctrl+F2")
    assert combobox.get() == "Ctrl+F2"

    notebook = FakeTtk.Notebook()
    assert notebook.add("plain") == "plain"
    assert notebook.add("common", text="常用功能") == "common"
    assert notebook.tabs["common"]["text"] == "Common tools"

    window = FakeTtk.Window()
    assert window.title() == "initial"
    assert window.title("选择游戏") is None
    assert window.current_title == "Choose game"
    assert window.title(123) == "title-result"
    assert window.current_title == 123

    i18n.set_language("es")
    i18n.refresh_widgets()

    assert combobox.options["values"] == [1, "Elegir juego"]
    assert notebook.tabs["common"]["text"] == "Herramientas comunes"
    assert window.current_title == "Elegir juego"
    i18n.set_language(i18n.DEFAULT_LANGUAGE)


def test_install_tk_i18n_tolerates_already_patched_or_minimal_widgets():
    class NoSelectionCombobox:
        def __init__(self, *args, **kwargs):
            del args
            self.options = dict(kwargs)

        def configure(self, **kwargs):
            self.options.update(kwargs)

    class AlreadyPatchedCombobox(NoSelectionCombobox):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._i18n_value_methods_patched = True

        def get(self):
            return ""

        def set(self, value):
            self.selected = value

    class AlreadyPatchedNotebook:
        def __init__(self, *args, **kwargs):
            del args, kwargs
            self._i18n_notebook_patched = True

        def add(self, child, **kwargs):
            del kwargs
            return child

    class WindowWithoutTitle:
        def __init__(self, *args, **kwargs):
            del args, kwargs

    class MinimalModule:
        Combobox = NoSelectionCombobox
        Notebook = AlreadyPatchedNotebook
        Window = WindowWithoutTitle

    class AlreadyPatchedModule:
        Combobox = AlreadyPatchedCombobox

    i18n.set_language("en")
    i18n.install_tk_i18n(MinimalModule)
    i18n.install_tk_i18n(AlreadyPatchedModule)

    combo = MinimalModule.Combobox(values=["选择游戏"])
    assert combo.options["values"] == ["Choose game"]
    assert MinimalModule.Notebook().add("tab", text="常用功能") == "tab"
    assert isinstance(MinimalModule.Window(), WindowWithoutTitle)

    already_patched = AlreadyPatchedModule.Combobox(values=["选择游戏"])
    assert already_patched.options["values"] == ["Choose game"]
    assert already_patched.get() == ""
    i18n.set_language(i18n.DEFAULT_LANGUAGE)


def test_refresh_widgets_drops_stale_widget_notebook_and_window_registrations():
    class FailsAfterRegister:
        def __init__(self):
            self.fail = False
            self.options = {}

        def configure(self, **kwargs):
            if self.fail:
                raise RuntimeError("stale widget")
            self.options.update(kwargs)

    class FailingNotebook:
        def __init__(self):
            self.fail = False
            self.tabs = {"tab": {}}

        def tab(self, child, **kwargs):
            if self.fail:
                raise RuntimeError("stale notebook")
            self.tabs[child].update(kwargs)

    class FailingWindow:
        def __init__(self):
            self.fail = False
            self.current_title = ""

        def title(self, text=None):
            if text is None:
                return self.current_title
            if self.fail:
                raise RuntimeError("stale window")
            self.current_title = text

    widget = FailsAfterRegister()
    notebook = FailingNotebook()
    window = FailingWindow()
    i18n.set_language("en")

    i18n.register_widget(widget, text="选择游戏")
    i18n.register_notebook_tab(notebook, "tab", "常用功能")
    i18n.register_window_title(window, "选择游戏")

    widget.fail = True
    notebook.fail = True
    window.fail = True

    i18n.refresh_widgets()
    i18n.refresh_widgets()

    assert widget.options["text"] == "Choose game"
    assert notebook.tabs["tab"]["text"] == "Common tools"
    assert window.current_title == "Choose game"
    i18n.set_language(i18n.DEFAULT_LANGUAGE)


def test_value_refresh_tolerates_widgets_without_working_get_or_set():
    class WidgetWithoutGet:
        def __init__(self):
            self.options = {}

        def configure(self, **kwargs):
            self.options.update(kwargs)

    class WidgetWithBrokenGet(WidgetWithoutGet):
        def get(self):
            raise RuntimeError("broken get")

    class WidgetWithoutSet(WidgetWithoutGet):
        def get(self):
            return "选择游戏"

    class WidgetWithBrokenSet(WidgetWithoutSet):
        def set(self, value):
            del value
            raise RuntimeError("broken set")

    i18n.set_language("en")
    widgets = [
        WidgetWithoutGet(),
        WidgetWithBrokenGet(),
        WidgetWithoutSet(),
        WidgetWithBrokenSet(),
    ]

    for widget in widgets:
        i18n.register_widget(widget, values=["选择游戏"])
    i18n.refresh_widgets()

    for widget in widgets:
        assert widget.options["values"] == ["Choose game"]
    i18n.set_language(i18n.DEFAULT_LANGUAGE)


def test_translated_combobox_values_keep_source_values_for_business_logic():
    class FakeCombobox:
        def __init__(self, *args, **kwargs):
            del args
            self.options = dict(kwargs)
            self.selected = ""

        def configure(self, **kwargs):
            self.options.update(kwargs)

        def get(self):
            return self.selected

        def set(self, value):
            self.selected = value

    class FakeTtk:
        Combobox = FakeCombobox

    i18n.set_language("en")
    i18n.install_tk_i18n(FakeTtk)

    combobox = FakeTtk.Combobox(values=["选择游戏", "植物"])
    combobox.set("植物")

    assert combobox.options["values"] == ["Choose game", "Plants"]
    assert combobox.selected == "Plants"
    assert combobox.get() == "植物"

    i18n.set_language("es")
    i18n.refresh_widgets()

    assert combobox.options["values"] == ["Elegir juego", "Plantas"]
    assert combobox.selected == "Plantas"
    assert combobox.get() == "植物"
