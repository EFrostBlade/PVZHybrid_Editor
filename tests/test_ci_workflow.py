from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
RELEASE_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "release.yml"


def test_ci_workflow_runs_free_hosted_python_test_gate():
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "runs-on: ubuntu-latest" in workflow
    assert "actions/checkout@v7" in workflow
    assert "actions/setup-python@v6" in workflow
    assert "cache: pip" in workflow
    assert "cache-dependency-path: requirements-dev.txt" in workflow
    assert (
        "python -m ruff check editor_config.py editor_ui_smoke.py i18n.py i18n_audit.py "
        "editor_layout_audit.py editor_runtime.py release_package.py responsive_tk.py "
        "responsive_ui_smoke.py tests"
    ) in workflow
    assert "python -m coverage run -m pytest -q" in workflow
    assert "python -m coverage report" in workflow


def test_release_workflow_builds_standard_and_win7_windows_test_artifacts():
    workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")

    assert "name: Build Windows Test EXE" in workflow
    assert "push:\n  pull_request:" in workflow
    assert "branches:" not in workflow
    assert "tags:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "build-standard-windows-exe:" in workflow
    assert "name: Windows standard executable" in workflow
    assert "python-version: \"3.12\"" in workflow
    assert "architecture: \"x64\"" in workflow
    assert "runs-on: windows-latest" in workflow
    assert "actions/checkout@v7" in workflow
    assert "actions/setup-python@v6" in workflow
    assert "https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe" in workflow
    assert "python-3.8.10-win32" in workflow
    assert "Include_pip=1" in workflow
    assert "platform.architecture()[0] != \"32bit\"" in workflow
    assert "sys.version_info[:2] != (3, 8)" in workflow
    assert "& $python -m pip install -r requirements.txt" in workflow
    assert "& $python -m pip install pyinstaller" in workflow
    assert "pyinstaller" in workflow
    assert "--onefile" in workflow
    assert "--windowed" in workflow
    assert "--icon res/icon/editor.ico" in workflow
    assert "--add-data" in workflow
    assert "locales:locales" in workflow
    assert "res:res" in workflow
    assert "git rev-parse HEAD" in workflow
    assert "PVZHybrid_Editor_b${{ steps.build_version.outputs.version }}" in workflow
    assert "win7_x86.PVZHybrid_Editor_b${{ steps.build_version.outputs.version }}" in workflow
    assert "release_package.py" in workflow
    assert "--version \"${{ steps.build_version.outputs.version }}\"" in workflow
    assert "--no-platform-tag" in workflow
    assert "--platform-tag win7_x86" in workflow
    assert "--github-output $env:GITHUB_OUTPUT" in workflow
    assert "actions/upload-artifact@v7" in workflow
    assert "name: ${{ steps.package.outputs.exe_name }}" in workflow
    assert "name: ${{ steps.package.outputs.sha_name }}" in workflow
    assert "name: ${{ steps.package.outputs.manifest_name }}" in workflow
    assert "archive: false" not in workflow
    assert "release-assets:" not in workflow
    assert "permissions:\n      contents: write" not in workflow
    assert "actions/download-artifact@v8" not in workflow
    assert "GH_REPO: ${{ github.repository }}" not in workflow
    assert "gh release" not in workflow


def test_release_workflow_captures_windows_responsive_ui_smoke_screenshot():
    workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")

    assert "responsive-ui-smoke:" in workflow
    assert "name: Windows responsive UI smoke" in workflow
    assert "runs-on: windows-latest" in workflow
    assert "actions/setup-python@v6" in workflow
    assert "python responsive_ui_smoke.py --output-dir ui-smoke-artifacts" in workflow
    assert "ui-smoke-artifacts/responsive-ui-smoke.png" in workflow
    assert "ui-smoke-artifacts/responsive-ui-smoke.json" in workflow


def test_release_workflow_captures_actual_editor_ui_smoke_screenshot():
    workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")

    assert "actual-editor-ui-smoke:" in workflow
    assert "name: Windows actual editor UI smoke" in workflow
    assert "runs-on: windows-latest" in workflow
    assert "python -m pip install -r requirements.txt" in workflow
    assert "python editor_ui_smoke.py --output-dir editor-ui-smoke-artifacts" in workflow
    assert "editor-ui-smoke-artifacts/editor-ui-smoke.png" in workflow
    assert "editor-ui-smoke-artifacts/editor-ui-smoke.json" in workflow
