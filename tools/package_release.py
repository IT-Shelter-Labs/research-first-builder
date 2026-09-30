"""Build clean, reproducible local archives without private workspace/config/cache files."""

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0-rc1"
ALLOWED_FOLDERS = {"skills", "tests", "examples", "tools", "evals", "docs", "media", ".github"}
ALLOWED_ROOT = {
    "README.md",
    "README_RU.md",
    "LICENSE",
    "AGENTS.md",
    ".gitignore",
    ".gitattributes",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
    "ruff.toml",
    "requirements-dev.txt",
}


def files(directory):
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if any(part in {"__pycache__", ".git", ".venv", "dist"} for part in relative.parts):
            continue
        if path.is_symlink():
            raise RuntimeError("Do not package symlinks")
        if path.is_file() and path.suffix not in {".pyc", ".pyo", ".db"}:
            yield path


def archive(destination, entries):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path, name in entries:
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            package.writestr(info, path.read_bytes())
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def main():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    full = []
    for path in files(ROOT):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in ALLOWED_FOLDERS or relative.as_posix() in ALLOWED_ROOT:
            full.append((path, "research-first-builder/" + relative.as_posix()))
    skill = ROOT / "skills" / "research-first-build"
    products = [
        (output / f"research-first-builder-{VERSION}.zip", full),
        (
            output / f"research-first-build-skill-{VERSION}.zip",
            [
                (path, "research-first-build/" + path.relative_to(skill).as_posix())
                for path in files(skill)
            ],
        ),
    ]
    sums = []
    for path, entries in products:
        digest = archive(path, entries)
        sums.append(digest + "  " + path.name)
        print(f"{path.name}: {len(entries)} files, {path.stat().st_size} bytes")
    (output / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
