import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
DEV_REQUIREMENTS = REPO_ROOT / "requirements-dev.txt"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def test_coverage_gate_requires_full_typed_core_coverage():
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    requirements = DEV_REQUIREMENTS.read_text(encoding="utf-8")
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "coverage[toml]>=" in requirements

    coverage_run = pyproject["tool"]["coverage"]["run"]
    assert coverage_run["branch"] is True
    assert coverage_run["source"] == [
        "editor_config",
        "editor_ui_smoke",
        "i18n",
        "i18n_audit",
        "editor_layout_audit",
        "editor_runtime",
        "release_package",
        "responsive_tk",
        "responsive_ui_smoke",
    ]

    coverage_report = pyproject["tool"]["coverage"]["report"]
    assert coverage_report["fail_under"] == 100
    assert coverage_report["show_missing"] is True

    assert "python -m coverage run -m pytest -q" in workflow
    assert "python -m coverage report" in workflow
