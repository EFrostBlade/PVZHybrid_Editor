import json
from pathlib import Path

import pytest

import responsive_ui_smoke


def test_build_audit_records_window_scroll_and_pixel_evidence():
    audit = responsive_ui_smoke.build_audit(
        screenshot_path=Path("responsive-ui-smoke.png"),
        screenshot_size_bytes=2048,
        screenshot_varies=True,
        window_width=900,
        window_height=720,
        canvas_width=850,
        canvas_height=640,
        scrollregion=(0, 0, 900, 650),
    )

    assert audit.screenshot_name == "responsive-ui-smoke.png"
    assert audit.screenshot_size_bytes == 2048
    assert audit.screenshot_varies is True
    assert audit.window_width == 900
    assert audit.window_height == 720
    assert audit.min_content_width == 900
    assert audit.min_content_height == 650
    assert audit.horizontal_scroll_available is True
    assert audit.vertical_scroll_available is True


def test_write_audit_json_uses_stable_keys(tmp_path):
    audit = responsive_ui_smoke.SmokeAudit(
        screenshot_name="responsive-ui-smoke.png",
        screenshot_size_bytes=2048,
        screenshot_varies=True,
        window_width=900,
        window_height=720,
        canvas_width=850,
        canvas_height=640,
        min_content_width=900,
        min_content_height=650,
        scrollregion=[0, 0, 900, 650],
        horizontal_scroll_available=True,
        vertical_scroll_available=True,
    )
    output = tmp_path / "audit.json"

    responsive_ui_smoke.write_audit(output, audit)

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "screenshot_name": "responsive-ui-smoke.png",
        "screenshot_size_bytes": 2048,
        "screenshot_varies": True,
        "window_width": 900,
        "window_height": 720,
        "canvas_width": 850,
        "canvas_height": 640,
        "min_content_width": 900,
        "min_content_height": 650,
        "scrollregion": [0, 0, 900, 650],
        "horizontal_scroll_available": True,
        "vertical_scroll_available": True,
    }


def test_assert_screenshot_evidence_rejects_blank_or_missing_file(tmp_path):
    screenshot = tmp_path / "responsive-ui-smoke.png"

    try:
        responsive_ui_smoke.assert_screenshot_evidence(screenshot, screenshot_varies=True)
    except FileNotFoundError as error:
        assert "responsive-ui-smoke.png" in str(error)
    else:
        raise AssertionError("missing screenshot should fail")

    screenshot.write_bytes(b"x" * 200)

    try:
        responsive_ui_smoke.assert_screenshot_evidence(screenshot, screenshot_varies=False)
    except ValueError as error:
        assert "blank screenshot" in str(error)
    else:
        raise AssertionError("blank screenshot should fail")

    responsive_ui_smoke.assert_screenshot_evidence(screenshot, screenshot_varies=True)


def test_assert_screenshot_evidence_rejects_too_small_file(tmp_path):
    screenshot = tmp_path / "responsive-ui-smoke.png"
    screenshot.write_bytes(b"x")

    try:
        responsive_ui_smoke.assert_screenshot_evidence(screenshot, screenshot_varies=True)
    except ValueError as error:
        assert "too small" in str(error)
    else:
        raise AssertionError("tiny screenshot should fail")


def test_main_runs_smoke_with_output_dir(monkeypatch, tmp_path):
    captured = {}

    def fake_run_smoke(output_dir):
        captured["output_dir"] = output_dir
        return responsive_ui_smoke.SmokeAudit(
            screenshot_name="responsive-ui-smoke.png",
            screenshot_size_bytes=2048,
            screenshot_varies=True,
            window_width=900,
            window_height=720,
            canvas_width=850,
            canvas_height=640,
            min_content_width=900,
            min_content_height=650,
            scrollregion=[0, 0, 900, 650],
            horizontal_scroll_available=True,
            vertical_scroll_available=True,
        )

    monkeypatch.setattr(responsive_ui_smoke, "run_smoke", fake_run_smoke)

    assert responsive_ui_smoke.main(["--output-dir", str(tmp_path)]) == 0
    assert captured == {"output_dir": tmp_path}


def test_main_requires_output_dir():
    with pytest.raises(SystemExit):
        responsive_ui_smoke.main([])
