import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
DEV_REQUIREMENTS = REPO_ROOT / "requirements-dev.txt"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def test_mypy_gate_covers_typed_core_modules():
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    requirements = DEV_REQUIREMENTS.read_text(encoding="utf-8")
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "mypy>=" in requirements

    mypy_config = pyproject["tool"]["mypy"]
    assert mypy_config["python_version"] == "3.11"
    assert mypy_config["files"] == [
        "editor_config.py",
        "editor_ui_smoke.py",
        "i18n.py",
        "i18n_audit.py",
        "editor_layout_audit.py",
        "editor_runtime.py",
        "release_package.py",
        "responsive_tk.py",
        "responsive_ui_smoke.py",
    ]
    assert mypy_config["disallow_untyped_defs"] is True
    assert mypy_config["check_untyped_defs"] is True
    assert mypy_config["warn_return_any"] is True
    assert mypy_config["strict"] is True

    assert "python -m mypy" in workflow
