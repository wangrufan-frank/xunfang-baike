"""Copy selected non-runtime outputs to an external archive with verification."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


MANIFEST_NAME = "manifest.tsv"
MANIFEST_HEADER = "sha256\tbytes\tpath\n"
CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_name(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path == Path("."):
        raise ValueError(f"archive path must be a relative directory name: {value}")
    return path


def inventory(root: Path, names: list[Path]) -> list[tuple[str, int, str]]:
    rows: list[tuple[str, int, str]] = []
    for name in names:
        for path in sorted((root / name).rglob("*")):
            if path.is_file():
                rows.append(
                    (
                        path.relative_to(root).as_posix(),
                        path.stat().st_size,
                        sha256_file(path),
                    )
                )
    return rows


def manifest_bytes(rows: list[tuple[str, int, str]]) -> bytes:
    lines = [MANIFEST_HEADER]
    lines.extend(f"{digest}\t{size}\t{relative}\n" for relative, size, digest in rows)
    return "".join(lines).encode("utf-8")


def archive(source_root: Path, archive_root: Path, names: list[Path]) -> bytes:
    source_root = source_root.resolve(strict=True)
    archive_root = archive_root.resolve()
    if source_root == archive_root:
        raise ValueError("archive root must differ from source root")
    if archive_root.exists() and any(archive_root.iterdir()):
        raise ValueError(f"archive root is not empty: {archive_root}")
    for name in names:
        source = source_root / name
        if not source.is_dir():
            raise ValueError(f"source directory does not exist: {source}")

    archive_root.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(source_root / name, archive_root / name)

    source_rows = inventory(source_root, names)
    archive_rows = inventory(archive_root, names)
    if source_rows != archive_rows:
        raise RuntimeError("archive verification failed: source and archive inventories differ")

    data = manifest_bytes(source_rows)
    (archive_root / MANIFEST_NAME).write_bytes(data)
    return data


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy selected deliverable directories and verify SHA-256 hashes."
    )
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--path", action="append", required=True)
    parser.add_argument("--manifest-copy", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        names = [source_name(value) for value in args.path]
        if len(set(names)) != len(names):
            raise ValueError("archive paths must be unique")
        data = archive(args.source_root, args.archive_root, names)
        if args.manifest_copy:
            args.manifest_copy.parent.mkdir(parents=True, exist_ok=True)
            args.manifest_copy.write_bytes(data)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ARCHIVE_ERROR {error}", file=sys.stderr)
        return 1

    print(f"ARCHIVE_OK {len(data.splitlines()) - 1} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
