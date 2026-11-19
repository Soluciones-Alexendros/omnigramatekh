#!/usr/bin/env python3
"""Comprueba que los enlaces relativos de la documentación resuelven a algo.

Solo valida rutas: los anclas (#seccion) y las URLs externas no se comprueban
(las primeras son frágiles, las segundas requieren red).

Uso:
    python3 scripts/check_links.py [rutas...]

Sin argumentos revisa todos los .md rastreados por git.
Exit codes:
    0 = todo resuelve
    1 = hay enlaces rotos
    2 = argumento no es fichero existente
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".archify"}
# Fences: ``` ... ``` y ~~~ ... ~~~
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
# Inline links: [text](path)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Reference links: [id]: path (at line start, optional whitespace)
REF_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.M)


def tracked_markdown() -> list[Path]:
    try:
        out = subprocess.run(  # noqa: S603
            [shutil.which("git") or "git", "ls-files", "*.md"],
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


def is_absolute_path(target: str) -> bool:
    return target.startswith("/")


def escapes_repo(target: str, base: Path) -> bool:
    """True si el target resuelve fuera del REPO."""
    try:
        resolved = (base / unquote(target)).resolve()
        # Comprobar que resolved está dentro de REPO
        resolved.relative_to(REPO)
        return False
    except ValueError:
        # relative_to lanza ValueError si no está dentro
        return True


def normalize(path: Path) -> str:
    # Compara en NFC: hay ficheros con acentos y macOS usa NFD.
    return unicodedata.normalize("NFC", str(path))


def make_origin(md: Path) -> str:
    try:
        return str(md.relative_to(REPO))
    except ValueError:
        return str(md)


def check_file(md: Path) -> list[tuple[int, str, str, str | None]]:
    problems: list[tuple[int, str, str, str | None]] = []
    try:
        text = md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        problems.append((0, str(md), "no es UTF-8", None))
        return problems

    clean = strip_noise(text)
    origin = make_origin(md)

    # Inline links
    for match in LINK_RE.finditer(clean):
        target = match.group(1)
        if is_external(target):
            continue
        if is_absolute_path(target):
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, "ruta absoluta"))
            continue
        if escapes_repo(target, md.parent):
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, "escapa del repo"))
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md.parent / unquote(path_part)).resolve()
        if not Path(normalize(resolved)).exists():
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, None))

    # Reference links: [id]: path
    for match in REF_LINK_RE.finditer(clean):
        target = match.group(1)
        if is_external(target):
            continue
        if is_absolute_path(target):
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, "ruta absoluta"))
            continue
        if escapes_repo(target, md.parent):
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, "escapa del repo"))
            continue
        resolved = (md.parent / unquote(target)).resolve()
        if not Path(normalize(resolved)).exists():
            line = text[: match.start()].count("\n") + 1
            problems.append((line, target, origin, None))

    return problems


def main(argv: list[str]) -> int:
    if argv:
        files = []
        for a in argv:
            p = Path(a)
            if not p.is_file():
                print(f"check_links: error: '{a}' no es un fichero existente", file=sys.stderr)
                return 2
            files.append(p)
    else:
        files = tracked_markdown()

    broken: list[tuple[int, str, str, str | None]] = []
    for md in files:
        broken.extend(check_file(md))

    if not broken:
        print(f"check_links: OK ({len(files)} ficheros Markdown, 0 enlaces rotos)")
        return 0

    print(f"check_links: {len(broken)} enlace(s) roto(s)", file=sys.stderr)
    for item in broken:
        if len(item) == 4 and item[3]:
            line, target, origin, reason = item
            print(f"  {origin}:{line} → {target} ({reason})", file=sys.stderr)
        else:
            line, target, origin, _ = item
            print(f"  {origin}:{line} → {target}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
