"""Translation behavior and work-count regressions; no Tk/display required."""
import types
import unittest
from unittest.mock import patch

import i18n


class Combo:
    def __init__(self, values=(), **kwargs):
        self.values = list(values)
        self.value = kwargs.get("textvariable", "")
        self.index = -1
        self.configurations = []

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.index = self.values.index(value) if value in self.values else -1

    def current(self, index=None):
        if index is not None:
            self.index = index
            self.value = self.values[index]
        return self.index

    def configure(self, **kwargs):
        self.configurations.append(kwargs)
        if "values" in kwargs:
            self.values = list(kwargs["values"])
            self.index = self.values.index(self.value) if self.value in self.values else -1


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.language = i18n.get_language()
        self.addCleanup(i18n.set_language, self.language)
        i18n.set_language("en")
        for name in ("_translate_template", "_segment_rules"):
            cached = getattr(i18n, name, None)
            if cached is not None:
                cached.cache_clear()
                self.addCleanup(cached.cache_clear)
        catalog = {"甲": "A", "乙": "B", "重复一": "same", "重复二": "same",
                   "数值 {value}": "Value {value}"}
        self.catalog = patch.object(i18n, "_load_catalog", side_effect=lambda code: catalog if code == "en" else {})
        self.loader = self.catalog.start()
        self.addCleanup(self.catalog.stop)
        self.module = types.ModuleType("test_widgets")
        self.module.Combobox = Combo
        i18n.install_tk_i18n(self.module)

    def test_empty_selection_never_translates_candidates(self):
        widget = self.module.Combobox(values=["甲", "乙"] * 300)
        with patch.object(i18n, "translate") as translate:
            self.assertEqual(widget.get(), "")
            self.assertEqual(translate.call_count, 0)

    def test_factory_does_not_reconfigure_already_translated_values(self):
        widget = self.module.Combobox(values=(v for v in ("甲", "乙")))
        self.assertEqual(widget.values, ["A", "B"])
        self.assertEqual(widget._i18n_original_values, ["甲", "乙"])
        self.assertEqual(widget.configurations, [])

    def test_repeated_translation_uses_cached_template(self):
        for _ in range(100):
            self.assertEqual(i18n.translate("甲"), "A")
        self.loader.assert_called_once_with("en")

    def test_factory_translates_preselected_source_without_reconfiguring(self):
        widget = self.module.Combobox(values=["甲", "乙"], textvariable="乙")
        self.assertEqual(widget.value, "B")
        self.assertEqual(widget.get(), "乙")
        self.assertEqual(widget.current(), 1)
        self.assertEqual(widget.configurations, [])

    def test_cache_separates_language_and_formats_after_lookup(self):
        self.assertEqual(i18n.translate("甲", language="en"), "A")
        self.assertEqual(i18n.translate("甲", language="zh_CN"), "甲")
        self.assertEqual(i18n.translate("数值 {value}", value=[1]), "Value [1]")
        self.assertEqual(i18n.translate("数值 {value}", value={"x": 2}), "Value {'x': 2}")

    def test_selected_duplicate_translation_keeps_actual_index(self):
        widget = self.module.Combobox(values=["重复一", "重复二"])
        widget.current(1)
        self.assertEqual(widget.get(), "重复二")
        i18n.set_language("zh_CN")
        i18n._apply_widget_translation(widget, i18n._widgets[widget])
        self.assertEqual(widget.current(), 1)
        self.assertEqual(widget.get(), "重复二")

    def test_dynamic_values_replace_source_metadata(self):
        widget = self.module.Combobox(values=["甲"])
        widget.current(0)
        i18n.register_widget(widget, values=["甲", "乙"])
        widget.current(1)
        self.assertEqual(widget.get(), "乙")
        i18n.register_widget(widget, values=["乙", "甲"])
        self.assertEqual(widget.current(), 0)
        self.assertEqual(widget.get(), "乙")

    def test_free_input_and_foreign_language_values_are_preserved(self):
        widget = self.module.Combobox(values=["甲", "乙"])
        i18n.set_language("zh_CN")
        i18n._apply_widget_translation(widget, i18n._widgets[widget])
        widget._i18n_original_set("B")
        self.assertEqual(widget.get(), "乙")
        widget.set("自定义内容")
        self.assertEqual(widget.get(), "自定义内容")
        i18n._apply_widget_translation(widget, i18n._widgets[widget])
        self.assertEqual(widget.get(), "自定义内容")

    def test_non_string_values_are_not_translated(self):
        widget = self.module.Combobox(values=[1, "甲"])
        widget.current(0)
        self.assertEqual(widget.get(), 1)

    def test_duplicate_sources_keep_the_selected_index(self):
        widget = self.module.Combobox(values=["甲", "甲"])
        widget.current(1)
        i18n._apply_widget_translation(widget, i18n._widgets[widget])
        self.assertEqual(widget.current(), 1)

    def test_failed_index_lookup_falls_back_to_string_matching(self):
        widget = self.module.Combobox(values=["甲", "乙"])
        widget.set("乙")
        with patch.object(widget, "current", side_effect=RuntimeError("no index")):
            self.assertEqual(widget.get(), "乙")

    def test_segment_rules_are_sorted_once_per_language(self):
        with patch("builtins.sorted", wraps=sorted) as sort:
            self.assertEqual(i18n.translate("甲一"), "A一")
            self.assertEqual(i18n.translate("甲二"), "A二")
        self.assertEqual(sort.call_count, 1)


if __name__ == "__main__":
    unittest.main()
