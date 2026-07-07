"""Prepare GitHub Actions release artifacts for the Windows executable."""
# ruff: noqa: UP017,UP045

from __future__ import annotations

import argparse
import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

APP_NAME = "PVZHybrid_Editor"
DEFAULT_PLATFORM_TAG = "win7_x86"


@dataclass(frozen=True)
class ReleasePackage:
    exe_name: str
    manifest_name: str
    sha_name: str
    exe_path: Path
    manifest_path: Path
    sha_path: Path
    sha256: str
    size_bytes: int
    size_mb: float
    date_label: str


def read_version(path: Path) -> str:
    version = path.read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError("version.txt is empty")
    return version


def executable_name(version: str, platform_tag: str = DEFAULT_PLATFORM_TAG) -> str:
    prefix = f"{platform_tag}." if platform_tag else ""
    return f"{prefix}{APP_NAME}_b{version}.exe"


def prepare_release_package(
    *,
    dist_dir: Path,
    version: str,
    built_at: date,
    github_output: Optional[Path] = None,
    platform_tag: str = DEFAULT_PLATFORM_TAG,
) -> ReleasePackage:
    exe_name = executable_name(version, platform_tag=platform_tag)
    exe_path = dist_dir / exe_name
    if not exe_path.exists():
        raise FileNotFoundError(f"Expected executable missing: {exe_path}")

    payload = exe_path.read_bytes()
    sha256 = hashlib.sha256(payload).hexdigest()
    size_bytes = len(payload)
    size_mb = round(size_bytes / (1024 * 1024), 1)
    date_label = f"{built_at:%b} {built_at.day}"

    manifest_name = f"{exe_name}.txt"
    sha_name = f"{exe_name}.sha256"
    manifest_path = dist_dir / manifest_name
    sha_path = dist_dir / sha_name

    manifest_path.write_text(
        "\n".join(
            [
                exe_name,
                f"sha256:{sha256}",
                str(size_bytes),
                f"{size_mb:.1f} MB",
                date_label,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    sha_path.write_text(f"sha256:{sha256}  {exe_name}\n", encoding="ascii")

    package = ReleasePackage(
        exe_name=exe_name,
        manifest_name=manifest_name,
        sha_name=sha_name,
        exe_path=exe_path,
        manifest_path=manifest_path,
        sha_path=sha_path,
        sha256=sha256,
        size_bytes=size_bytes,
        size_mb=size_mb,
        date_label=date_label,
    )
    if github_output is not None:
        write_github_output(github_output, package)
    return package


def write_github_output(path: Path, package: ReleasePackage) -> None:
    with path.open("a", encoding="utf-8") as output:
        output.write(
            "\n".join(
                [
                    f"exe_name={package.exe_name}",
                    f"manifest_name={package.manifest_name}",
                    f"sha_name={package.sha_name}",
                    f"exe_path={package.exe_path}",
                    f"manifest_path={package.manifest_path}",
                    f"sha_path={package.sha_path}",
                ]
            )
            + "\n"
        )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist-dir", type=Path, required=True)
    version_group = parser.add_mutually_exclusive_group(required=True)
    version_group.add_argument("--version-file", type=Path)
    version_group.add_argument("--version")
    parser.add_argument("--github-output", type=Path)
    platform_group = parser.add_mutually_exclusive_group()
    platform_group.add_argument("--platform-tag", default=DEFAULT_PLATFORM_TAG)
    platform_group.add_argument("--no-platform-tag", action="store_true")
    parser.add_argument("--built-at")
    args = parser.parse_args(argv)

    version = args.version
    if version is not None:
        version = version.strip()
        if not version:
            raise ValueError("version is empty")
    else:
        version = read_version(args.version_file)

    built_at = _parse_date(args.built_at)
    prepare_release_package(
        dist_dir=args.dist_dir,
        version=version,
        built_at=built_at,
        github_output=args.github_output,
        platform_tag="" if args.no_platform_tag else args.platform_tag,
    )
    return 0


def _parse_date(value: Optional[str]) -> date:
    if value is None:
        return datetime.now(timezone.utc).date()
    return date.fromisoformat(value)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
