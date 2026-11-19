#!/usr/bin/env python3
"""Módulo común para scripts LinkML: helpers compartidos, exit codes, discovery.

Elimina duplicación entre validate_cycle.py y linkml_env.py (D-012).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import TypedDict

# Exit codes canónicos (usados por ambos scripts)
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INPUT = 2      # argumento inválido, fichero no existe, etc.
EXIT_MISSING = 3    # dependencia ausente (linkml, PyYAML, etc.)
EXIT_PERM = 4       # permiso denegado (binario no ejecutable)


class RunResult(TypedDict):
    exit_code: int
    stdout: str
    stderr: str


def find_linkml(linkml_arg: str | None, venv_dir: str | None) -> str | None:
    """Descubre el binario linkml.

    Prioridad:
    1. --linkml explícito (si existe; si no existe → None = error)
    2. --venv-dir/bin/linkml (si venv_dir dado pero no existe o no hay linkml → None = error)
    3. PATH (shutil.which) - solo si NO se dio --linkml ni --venv-dir

    Retorna None si no se encuentra (el caller decide exit code).
    """
    if linkml_arg:
        path = Path(linkml_arg)
        if not path.exists():
            return None
        return str(path)
    if venv_dir:
        cand = Path(venv_dir) / "bin" / "linkml"
        if cand.exists():
            return str(cand)
        # venv_dir explícito pero no existe linkml → error
        return None
    return shutil.which("linkml")


def run(cmd: list[str]) -> RunResult:
    """Ejecuta comando y retorna (exit_code, stdout, stderr).

    Envuelve subprocess.run con try/except para OSError (permiso, no encontrado).
    """
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa: S603
        return {"exit_code": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    except OSError as e:
        # PermissionError (13), FileNotFoundError (2), etc.
        return {"exit_code": EXIT_PERM, "stdout": "", "stderr": str(e)}


def parse_common_args(parser_name: str) -> argparse.Namespace:
    """Parser base compartido para argumentos comunes."""
    parser = argparse.ArgumentParser(description=parser_name)
    parser.add_argument("--venv-dir", help="virtualenv directory (bin/linkml inside)")
    parser.add_argument("--linkml", help="linkml executable (overrides discovery)")
    parser.add_argument("--json", action="store_true", help="JSON output instead of Markdown")
    return parser.parse_args()


def verify_executable(path: str) -> tuple[bool, str]:
    """Verifica que el binario existe y es ejecutable.

    Returns: (ok, detail)
    """
    p = Path(path)
    if not p.exists():
        return False, f"no existe: {path}"
    if not p.is_file():
        return False, f"no es un fichero: {path}"
    if not p.stat().st_mode & 0o111:  # check execute bit
        return False, f"no ejecutable (permiso): {path}"
    return True, "ok"
