#!/usr/bin/env python3
"""Gates de CONTRATO, no de presencia (MEJORA-04).

Comprueba coherencia que un «existe el fichero» no detecta:

  C1  package.json versión  ==  primera entrada de CHANGELOG (## [x.y.z])
  C2  Si README.md declara versión explícita, coincide con package.json
  C3  Cada job de ci.yml tiene al menos un `run:` no trivial o un `uses:` válido
  C4  Cada enlace de directorio en docs/README.md apunta a un directorio con
      contenido real (al menos un fichero que no sea .gitkeep)
  C5  Todo `uses:` de los workflows está fijado por SHA de 40 hex

No requiere PyYAML: el parseo de workflows es deliberadamente conservador y se
limita a lo que estos contratos necesitan (indentación de jobs y `uses:`).

Uso: python3 scripts/check_contracts.py [--root DIR]

Exit: 0 OK · 1 contrato incumplido · 2 error de uso.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?"
CHANGELOG_ENTRY = re.compile(rf"^## \[({SEMVER})\]", re.MULTILINE)
README_VERSION = re.compile(rf"Versi[oó]n\s+\**({SEMVER})\**", re.IGNORECASE)
JOB_LINE = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)")
RUN_LINE = re.compile(r"^\s*(?:-\s*)?run:\s*(.*)$")
DOC_DIR_LINK = re.compile(r"\]\(([A-Za-z0-9_./-]+)/\)")

# Comandos que no verifican nada: cuentan como ausencia de `run` real.
TRIVIAL_RUN = {"", "true", ":", "exit 0", "echo", "echo ok", 'echo "ok"'}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def package_version(root: Path) -> str | None:
    try:
        data = json.loads((root / "package.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    version = data.get("version")
    return version if isinstance(version, str) else None


def changelog_versions(text: str) -> list[str]:
    return [m.group(1) for m in CHANGELOG_ENTRY.finditer(text)]


def check_versions(root: Path) -> list[str]:
    problems: list[str] = []
    pkg = package_version(root)
    if pkg is None:
        return ["C1: package.json sin campo version válido"]

    versions = changelog_versions(read(root / "CHANGELOG.md"))
    if not versions:
        problems.append("C1: CHANGELOG.md sin ninguna entrada '## [x.y.z]'")
    elif versions[0] != pkg:
        problems.append(f"C1: package.json {pkg} != CHANGELOG primera entrada {versions[0]}")

    readme = read(root / "README.md")
    declared = {m.group(1) for m in README_VERSION.finditer(readme)}
    if declared and pkg not in declared:
        problems.append(f"C2: README declara {sorted(declared)} y package.json es {pkg}")

    return problems


def workflow_jobs(text: str) -> dict[str, list[str]]:
    """Devuelve {job: [líneas del bloque]} leyendo solo bajo la clave `jobs:`.

    Las claves de 2 espacios antes de `jobs:` pertenecen a `on:` (push,
    pull_request, schedule...), no son jobs.
    """
    jobs: dict[str, list[str]] = {}
    current: str | None = None
    in_jobs = False
    for line in text.splitlines():
        if not in_jobs:
            if re.match(r"^jobs:\s*$", line):
                in_jobs = True
            continue
        match = JOB_LINE.match(line)
        if match:
            current = match.group(1)
            jobs[current] = []
            continue
        # Fin del bloque jobs: clave de nivel raíz no comentada.
        if line and not line[0].isspace() and not line.startswith("#"):
            break
        if current is not None:
            jobs[current].append(line)
    return jobs


def normalize_command(raw: str) -> str:
    """Normaliza el valor de un `run:` para detectar comandos triviales."""
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def check_jobs(root: Path) -> list[str]:
    problems: list[str] = []
    wf_dir = root / ".github" / "workflows"
    files = sorted(wf_dir.glob("*.yml")) + sorted(wf_dir.glob("*.yaml"))
    if not files:
        return ["C3: no hay workflows en .github/workflows"]

    for wf in files:
        text = read(wf)
        jobs = workflow_jobs(text)
        if not jobs:
            problems.append(f"C3: {wf.name} sin jobs detectables")
            continue
        for name, block in jobs.items():
            has_run = any(
                (m := RUN_LINE.match(line)) and normalize_command(m.group(1)) not in TRIVIAL_RUN
                for line in block
            )
            has_uses = any(USES_LINE.match(line) for line in block)
            if not (has_run or has_uses):
                problems.append(f"C3: {wf.name}:{name} no ejecuta nada real (sin run ni uses)")
    return problems


def check_pinned_uses(root: Path) -> list[str]:
    problems: list[str] = []
    sha = re.compile(r"^[0-9a-f]{40}$")
    for wf in sorted((root / ".github" / "workflows").glob("*.y*ml")):
        for lineno, line in enumerate(read(wf).splitlines(), 1):
            match = USES_LINE.match(line)
            if not match:
                continue
            ref = match.group(1).strip("'\"")
            if ref.startswith(("./", "docker://")):
                continue
            if "@" not in ref or not sha.match(ref.rsplit("@", 1)[1]):
                problems.append(f"C5: {wf.name}:{lineno} uses sin SHA: {ref}")
    return problems


def check_docs_links(root: Path) -> list[str]:
    problems: list[str] = []
    docs_readme = root / "docs" / "README.md"
    targets = DOC_DIR_LINK.findall(read(docs_readme))
    if not targets:
        problems.append("C4: docs/README.md no enlaza ningún directorio")
    for target in targets:
        path = (docs_readme.parent / target).resolve()
        if not path.is_dir():
            problems.append(f"C4: docs/README.md enlaza {target}/, que no existe")
            continue
        real = [p for p in path.rglob("*") if p.is_file() and p.name != ".gitkeep"]
        if not real:
            problems.append(f"C4: {target}/ está vacío (solo .gitkeep o nada)")
    return problems


CHECKS = (
    ("versiones", check_versions),
    ("jobs de CI", check_jobs),
    ("uses fijados por SHA", check_pinned_uses),
    ("docs con contenido", check_docs_links),
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Gates de contrato (no de presencia).")
    parser.add_argument("--root", default=None, help="raíz del repo (por defecto, la del script)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        print(f"check_contracts: error: no es un directorio: {root}", file=sys.stderr)
        return 2

    problems: list[str] = []
    for label, check in CHECKS:
        found = check(root)
        status = "OK " if not found else "FAIL"
        print(f"[{status}] {label}")
        problems.extend(found)

    if problems:
        print("", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print(f"\ncheck_contracts: {len(problems)} contrato(s) incumplido(s)", file=sys.stderr)
        return 1

    print("\ncheck_contracts: OK (contratos de versión, CI y docs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
