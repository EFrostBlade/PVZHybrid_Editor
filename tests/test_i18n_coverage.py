from pathlib import Path

import i18n
import i18n_audit

REPO_ROOT = Path(__file__).resolve().parents[1]
EDITOR = REPO_ROOT / "editor.py"
LOCALES_DIR = REPO_ROOT / "locales"


def test_all_static_editor_ui_texts_are_in_every_locale_catalog():
    source_texts = i18n_audit.extract_static_ui_texts(EDITOR)

    assert len(source_texts) >= 300

    missing_by_locale = i18n_audit.missing_locale_keys(
        locale_dir=LOCALES_DIR,
        source_texts=source_texts,
        language_codes=[language.code for language in i18n.supported_languages()],
    )

    assert missing_by_locale == {}


def test_i18n_audit_reports_missing_locale_keys(tmp_path):
    locale_dir = tmp_path / "locales"
    locale_dir.mkdir()
    (locale_dir / "en.json").write_text(
        '{"translations": {"已翻译": "Translated"}}',
        encoding="utf-8",
    )

    missing_by_locale = i18n_audit.missing_locale_keys(
        locale_dir=locale_dir,
        source_texts={"已翻译", "未翻译"},
        language_codes=["en"],
    )

    assert missing_by_locale == {"en": ["未翻译"]}


def test_i18n_audit_ignores_title_calls_without_text(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        "\n".join(
            [
                "root.title()",
                "root.title('标题')",
                "label(text='文案')",
                "combo(values=('选项', 'Ctrl+F2'))",
                "button(text=dynamic_text)",
            ]
        ),
        encoding="utf-8",
    )

    assert i18n_audit.extract_static_ui_texts(source) == {"标题", "文案", "选项"}
