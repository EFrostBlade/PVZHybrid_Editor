import hashlib
from datetime import date

import pytest

import release_package


def test_prepare_release_package_writes_manifest_checksum_and_github_outputs(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    exe_name = "win7_x86.PVZHybrid_Editor_b0.73.exe"
    exe_path = dist_dir / exe_name
    payload = b"pvz hybrid editor"
    exe_path.write_bytes(payload)
    github_output = tmp_path / "github_output.txt"
    github_output.write_text("existing=value\n", encoding="utf-8")

    package = release_package.prepare_release_package(
        dist_dir=dist_dir,
        version="0.73",
        built_at=date(2026, 5, 10),
        github_output=github_output,
    )

    digest = hashlib.sha256(payload).hexdigest()
    assert package.exe_name == exe_name
    assert package.manifest_name == f"{exe_name}.txt"
    assert package.sha_name == f"{exe_name}.sha256"
    assert package.sha256 == digest
    assert package.size_bytes == len(payload)
    assert package.size_mb == 0.0
    assert package.date_label == "May 10"

    assert (dist_dir / f"{exe_name}.txt").read_text(encoding="utf-8").splitlines() == [
        exe_name,
        f"sha256:{digest}",
        str(len(payload)),
        "0.0 MB",
        "May 10",
    ]
    assert (dist_dir / f"{exe_name}.sha256").read_text(encoding="ascii") == (
        f"sha256:{digest}  {exe_name}\n"
    )
    assert github_output.read_text(encoding="utf-8").splitlines() == [
        "existing=value",
        f"exe_name={exe_name}",
        f"manifest_name={exe_name}.txt",
        f"sha_name={exe_name}.sha256",
        f"exe_path={dist_dir / exe_name}",
        f"manifest_path={dist_dir / f'{exe_name}.txt'}",
        f"sha_path={dist_dir / f'{exe_name}.sha256'}",
    ]


def test_prepare_release_package_rejects_missing_executable(tmp_path):
    with pytest.raises(FileNotFoundError, match="Expected executable missing"):
        release_package.prepare_release_package(
            dist_dir=tmp_path,
            version="0.73",
            built_at=date(2026, 5, 10),
        )


def test_prepare_release_package_can_skip_github_output(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "win7_x86.PVZHybrid_Editor_b0.73.exe").write_bytes(b"abc")

    package = release_package.prepare_release_package(
        dist_dir=dist_dir,
        version="0.73",
        built_at=date(2026, 5, 10),
    )

    assert package.exe_path.exists()
    assert package.manifest_path.exists()
    assert package.sha_path.exists()


def test_prepare_release_package_can_omit_platform_tag_for_standard_build(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    commit = "0123456789abcdef0123456789abcdef01234567"
    exe_name = f"PVZHybrid_Editor_b{commit}.exe"
    (dist_dir / exe_name).write_bytes(b"abc")

    package = release_package.prepare_release_package(
        dist_dir=dist_dir,
        version=commit,
        built_at=date(2026, 5, 10),
        platform_tag="",
    )

    assert package.exe_name == exe_name
    assert package.manifest_path.name == f"{exe_name}.txt"
    assert package.sha_path.name == f"{exe_name}.sha256"


def test_read_version_strips_whitespace_and_rejects_empty_file(tmp_path):
    version_file = tmp_path / "version.txt"
    version_file.write_text("  2.73\n", encoding="utf-8")
    assert release_package.read_version(version_file) == "2.73"

    version_file.write_text(" \n", encoding="utf-8")
    with pytest.raises(ValueError, match="version.txt is empty"):
        release_package.read_version(version_file)


def test_cli_prepares_package_and_writes_github_output(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    version_file = tmp_path / "version.txt"
    version_file.write_text("0.73\n", encoding="utf-8")
    (dist_dir / "win7_x86.PVZHybrid_Editor_b0.73.exe").write_bytes(b"abc")
    github_output = tmp_path / "github_output.txt"

    exit_code = release_package.main(
        [
            "--dist-dir",
            str(dist_dir),
            "--version-file",
            str(version_file),
            "--github-output",
            str(github_output),
            "--built-at",
            "2026-05-10",
        ]
    )

    assert exit_code == 0
    assert "sha_path=" in github_output.read_text(encoding="utf-8")


def test_cli_accepts_literal_commit_version_and_standard_build(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    commit = "0123456789abcdef0123456789abcdef01234567"
    exe_name = f"PVZHybrid_Editor_b{commit}.exe"
    (dist_dir / exe_name).write_bytes(b"abc")

    exit_code = release_package.main(
        [
            "--dist-dir",
            str(dist_dir),
            "--version",
            commit,
            "--no-platform-tag",
            "--built-at",
            "2026-05-10",
        ]
    )

    assert exit_code == 0
    assert (dist_dir / f"{exe_name}.txt").exists()


def test_cli_rejects_empty_literal_version(tmp_path):
    with pytest.raises(ValueError, match="version is empty"):
        release_package.main(
            [
                "--dist-dir",
                str(tmp_path),
                "--version",
                " ",
            ]
        )


def test_cli_uses_current_date_when_built_at_is_omitted(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    version_file = tmp_path / "version.txt"
    version_file.write_text("0.73\n", encoding="utf-8")
    exe_name = "win7_x86.PVZHybrid_Editor_b0.73.exe"
    (dist_dir / exe_name).write_bytes(b"abc")

    exit_code = release_package.main(
        [
            "--dist-dir",
            str(dist_dir),
            "--version-file",
            str(version_file),
        ]
    )

    assert exit_code == 0
    assert (dist_dir / f"{exe_name}.txt").exists()
