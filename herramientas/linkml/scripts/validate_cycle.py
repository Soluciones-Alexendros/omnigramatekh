#!/usr/bin/env python3
"""Ciclo de validación por capas para una skill data-linkml.

Capas 1-4 (sintaxis YAML → metamodelo → lint → instancia) con veredictos
esperados para casos positivos y negativos. Registra herramienta, versión,
comando, código de salida y resultado. Las capas 5-7 (conjunto/dominio,
artefacto, evidencia) quedan fuera: las cubren comprobadores propios del
proyecto (ver references/validation.md).

Convención de veredicto esperado por fichero de datos: si el nombre contiene
"invalid", se espera RECHAZO; en caso contrario, ACEPTACIÓN.

Exit codes canónicos: 0 OK, 1 error/veredicto negativo, 2 input inválido,
3 dependencia ausente, 4 permiso.

Uso:
  python3 validate_cycle.py --schema S.yaml --target-class C \
      --data a.yaml b-invalid.yaml [--linkml BIN] [--venv-dir DIR] [--json]
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

try:
    import yaml

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


class LayerDict(TypedDict):
    layer: int
    name: str
    status: str
    detail: str
    command: str | None
    exit_code: int | None
    expected: str | None
    actual: str | None
    file: str | None


class ReportDict(TypedDict):
    tool: str
    version: str
    binary: str
    schema: str
    target_class: str
    layers: list[LayerDict]
    verdict: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Layered LinkML validation cycle (data-linkml skill).")
    parser.add_argument("--schema", required=True, help="LinkML schema YAML file")
    parser.add_argument("--target-class", required=True, help="target class for instance validation")
    parser.add_argument("--data", nargs="+", required=True, help="instance data files")
    parser.add_argument("--linkml", help="linkml executable (overrides discovery)")
    parser.add_argument("--venv-dir", help="virtualenv directory (bin/linkml inside)")
    parser.add_argument("--json", action="store_true", help="JSON output instead of Markdown")
    return parser.parse_args()


def expected_verdict(filename: str) -> str:
    return "REJECT" if "invalid" in Path(filename).name.lower() else "ACCEPT"


def main() -> int:
    args = parse_args()
    schema = Path(args.schema)
    if not schema.is_file():
        print(f"ERROR: schema no encontrado: {schema}", file=sys.stderr)
        return EXIT_INPUT
    for data in args.data:
        if not Path(data).is_file():
            print(f"ERROR: fichero de datos no encontrado: {data}", file=sys.stderr)
            return EXIT_INPUT

    binpath = find_linkml(args.linkml, args.venv_dir)
    if not binpath:
        # Diferenciar: args explícitos → EXIT_INPUT; sin args → EXIT_MISSING
        if args.linkml or args.venv_dir:
            print(
                "ERROR: linkml no encontrado en la ruta especificada (--linkml/--venv-dir).",
                file=sys.stderr,
            )
            return EXIT_INPUT
        print(
            "ERROR: linkml CLI no encontrado. Instala con scripts/bootstrap_arch.sh o apunta --linkml/--venv-dir.",
            file=sys.stderr,
        )
        return EXIT_MISSING

    # Verificar que el binario es ejecutable
    ok, detail = verify_executable(binpath)
    if not ok:
        print(f"ERROR: linkml binario inválido: {detail}", file=sys.stderr)
        return EXIT_PERM

    version = "unknown"
    result = run([binpath, "--version"])
    if result["exit_code"] == 0:
        version = result["stdout"] or "unknown"

    report: ReportDict = {
        "tool": "linkml",
        "version": version,
        "binary": binpath,
        "schema": str(schema),
        "target_class": args.target_class,
        "layers": [],
        "verdict": "FAIL",
    }

    # Capa 1: sintaxis YAML (solo si PyYAML está disponible).
    if not HAS_YAML:
        report["layers"].append(
            {
                "layer": 1,
                "name": "yaml_syntax",
                "status": "not_run",
                "detail": "PyYAML no disponible; la sintaxis la cubrirá la capa 2 (linkml lint/validate)",
                "command": None,
                "exit_code": None,
                "expected": None,
                "actual": None,
                "file": None,
            }
        )
    else:
        try:
            with open(schema, encoding="utf-8") as fh:
                yaml.safe_load(fh)
            for data in args.data:
                with open(data, encoding="utf-8") as fh:
                    yaml.safe_load(fh)
            report["layers"].append(
                {
                    "layer": 1,
                    "name": "yaml_syntax",
                    "status": "pass",
                    "detail": "YAML bien formado",
                    "command": None,
                    "exit_code": None,
                    "expected": None,
                    "actual": None,
                    "file": None,
                }
            )
        except yaml.YAMLError as exc:
            report["layers"].append(
                {
                    "layer": 1,
                    "name": "yaml_syntax",
                    "status": "fail",
                    "detail": str(exc),
                    "command": None,
                    "exit_code": None,
                    "expected": None,
                    "actual": None,
                    "file": None,
                }
            )

    # Capa 2: metamodelo.
    cmd = [binpath, "validate", str(schema)]
    result = run(cmd)
    report["layers"].append(
        {
            "layer": 2,
            "name": "metamodel",
            "status": "pass" if result["exit_code"] == 0 else "fail",
            "command": " ".join(cmd),
            "exit_code": result["exit_code"],
            "detail": (result["stdout"] or result["stderr"])[:400],
            "expected": None,
            "actual": None,
            "file": None,
        }
    )

    # Capa 3: lint.
    cmd = [binpath, "lint", str(schema)]
    result = run(cmd)
    report["layers"].append(
        {
            "layer": 3,
            "name": "lint",
            "status": "pass" if result["exit_code"] == 0 else "fail",
            "command": " ".join(cmd),
            "exit_code": result["exit_code"],
            "detail": (result["stdout"] or result["stderr"])[:400],
            "expected": None,
            "actual": None,
            "file": None,
        }
    )

    # Capa 4: instancias, positivo y negativo.
    for data in args.data:
        cmd = [binpath, "validate", "-s", str(schema), "-C", args.target_class, data]
        result = run(cmd)
        actual = "ACCEPT" if result["exit_code"] == 0 else "REJECT"
        wanted = expected_verdict(data)
        ok = actual == wanted
        report["layers"].append(
            {
                "layer": 4,
                "name": "instance",
                "file": data,
                "expected": wanted,
                "actual": actual,
                "status": "pass" if ok else "fail",
                "command": " ".join(cmd),
                "exit_code": result["exit_code"],
                "detail": (result["stdout"] or result["stderr"])[:400],
            }
        )

    layers = report["layers"]
    # not_run en capa 1 es warn, no bloqueante (D-003)
    blocking = [layer for layer in layers if layer.get("status") == "fail" and layer.get("layer") in {1, 2, 3, 4}]
    report["verdict"] = "PASS" if not blocking else "FAIL"

    _emit(args, report)
    return EXIT_OK if report["verdict"] == "PASS" else EXIT_ERROR


def _emit(args: argparse.Namespace, report: ReportDict) -> None:
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("# LinkML validation cycle")
    print(f"- tool: {report['tool']} {report['version']} ({report['binary']})")
    print(f"- schema: {report['schema']} (target class {report['target_class']})")
    for layer in report["layers"]:
        mark = "OK " if layer.get("status") == "pass" else ("N/R" if layer.get("status") == "not_run" else "FAIL")
        extra = f" [{layer.get('expected')}→{layer.get('actual')}]" if layer.get("expected") else ""
        print(f"- [{mark}] L{layer['layer']} {layer['name']}{extra}: {layer.get('detail', '')}")
    print(f"Verdict: {report['verdict']}")


if __name__ == "__main__":
    sys.exit(main())
