#!/usr/bin/env python3
"""Comprueba que los enlaces relativos de la documentación resuelven a algo.

Solo valida rutas: los anclas (#seccion) y las URLs externas no se comprueban
(las primeras son frágiles, las segundas requieren red).

Uso:
    python3 scripts/check_links.py [rutas...]

Sin argumentos revisa todos los .md rastreados por git.
Exit: 0 si todo resuelve, 1 si hay enlaces rotos.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".archify"}
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def tracked_markdown() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return [REPO / line for line in out.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return sorted(p for p in REPO.rglob("*.md") if not SKIP_DIRS & set(p.parts))


def strip_noise(text: str) -> str:
    text = FENCE_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def is_external(target: str) -> bool:
    return (
        target.startswith(("http://", "https://", "//", "mailto:", "tel:", "#"))
        or "://" in target
    )


def normalize(path: Path) -> str:
    # Compara en NFC: hay ficheros con acentos y macOS usa NFD.
    return unicodedata.normalize("NFC", str(path))


def check_file(md: Path) -> list[tuple[int, str, str]]:
    problems: list[tuple[int, str, str]] = []
    try:
        text = md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        problems.append((0, str(md), "no es UTF-8"))
        return problems

    for match in LINK_RE.finditer(strip_noise(text)):
        target = match.group(1)
        if is_external(target):
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md.parent / unquote(path_part)).resolve()
        if not Path(normalize(resolved)).exists():
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, str(md.relative_to(REPO))))
    return problems


def main(argv: list[str]) -> int:
    if argv:
        files = [Path(a) for a in argv]
    else:
        files = tracked_markdown()

    broken: list[tuple[int, str, str]] = []
    for md in files:
        if not md.is_file():
            continue
        broken.extend(check_file(md))

    if not broken:
        print(f"check_links: OK ({len(files)} ficheros Markdown, 0 enlaces rotos)")
        return 0

    print(f"check_links: {len(broken)} enlace(s) roto(s)", file=sys.stderr)
    for line, target, origin in broken:
        print(f"  {origin}:{line} → {target}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
