#!/usr/bin/env python3
"""Pre-flight del entorno LinkML: Python y CLI presentes, versión, informe.

Exit codes canónicos: 0 OK, 1 error/veredicto negativo, 2 input inválido,
3 dependencia ausente, 4 permiso.

Uso:
  python3 linkml_env.py [--venv-dir DIR] [--json] [--linkml BIN]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TypedDict

# Importar helpers comunes
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from _common import EXIT_OK, EXIT_ERROR, EXIT_INPUT, EXIT_MISSING, EXIT_PERM, find_linkml, run, verify_executable

MIN_PYTHON = (3, 10)


class CheckDict(TypedDict):
    id: str
    ok: bool
    detail: str


class ReportDict(TypedDict):
    checks: list[CheckDict]
    verdict: str
    detail: str | None
    environment: dict[str, str] | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pre-flight LinkML environment check (data-linkml skill).")
    parser.add_argument("--venv-dir", help="virtualenv directory (bin/linkml inside)")
    parser.add_argument("--linkml", help="linkml executable to check (overrides discovery)")
    parser.add_argument("--json", action="store_true", help="JSON output instead of Markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report: ReportDict = {"checks": [], "verdict": "FAIL", "detail": None, "environment": None}

    py_ok = sys.version_info >= MIN_PYTHON
    report["checks"].append(
        {
            "id": "python",
            "ok": py_ok,
            "detail": f"python {sys.version.split()[0]} (>= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})",
        }
    )

    binpath = find_linkml(args.linkml, args.venv_dir)
    if not binpath:
        # Diferenciar: args explícitos → EXIT_INPUT; sin args → EXIT_MISSING
        if args.linkml or args.venv_dir:
            report["checks"].append(
                {
                    "id": "linkml_cli",
                    "ok": False,
                    "detail": "linkml no encontrado en la ruta especificada (--linkml/--venv-dir).",
                }
            )
            report["detail"] = "invalid input: linkml not found at specified path"
            _emit(args, report)
            return EXIT_INPUT
        report["checks"].append(
            {
                "id": "linkml_cli",
                "ok": False,
                "detail": (
                    "linkml CLI no encontrado: usa scripts/bootstrap_arch.sh "
                    "(Arch) o instala en un venv con el pin de assets/"
                    "requirements-linkml.txt"
                ),
            }
        )
        report["detail"] = "missing dependency: linkml CLI"
        _emit(args, report)
        return EXIT_MISSING

    # Verificar que el binario es ejecutable
    ok, detail = verify_executable(binpath)
    if not ok:
        report["checks"].append(
            {
                "id": "linkml_cli",
                "ok": False,
                "detail": f"binario inválido: {detail}",
            }
        )
        report["detail"] = f"linkml binary invalid: {detail}"
        _emit(args, report)
        return EXIT_PERM

    version = "unknown"
    result = run([binpath, "--version"])
    if result["exit_code"] == 0:
        version = result["stdout"] or "unknown"
    report["checks"].append(
        {
            "id": "linkml_cli",
            "ok": True,
            "detail": f"{binpath} --version -> {version}",
        }
    )

    if not py_ok:
        report["detail"] = "pre-flight failed: Python version"
        _emit(args, report)
        return EXIT_ERROR

    report["verdict"] = "PASS"
    report["environment"] = {"python": sys.version.split()[0], "linkml": version, "binary": binpath}
    _emit(args, report)
    return EXIT_OK


def _emit(args: argparse.Namespace, report: ReportDict) -> None:
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("# LinkML environment pre-flight")
    for check in report["checks"]:
        mark = "OK " if check["ok"] else "FAIL"
        print(f"- [{mark}] {check['id']}: {check['detail']}")
    env = report.get("environment")
    if env:
        print(f"- [OK ] environment: {env}")
    print(f"Verdict: {report['verdict']}")


if __name__ == "__main__":
    sys.exit(main())
