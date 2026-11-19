#!/usr/bin/env python3
"""Tests pytest para validate_cycle.py - caminos de error."""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]


def find_linkml() -> str | None:
    """Binario linkml disponible: venv del repo o PATH (CI lo instala global)."""
    import shutil

    cand = REPO_ROOT / ".venv" / "bin" / "linkml"
    if cand.is_file():
        return str(cand)
    return shutil.which("linkml")


VALIDATE_CYCLE = REPO_ROOT / "herramientas" / "linkml" / "scripts" / "validate_cycle.py"
LINKML_BIN = find_linkml()
SCHEMA = REPO_ROOT / "herramientas" / "linkml" / "assets" / "schema-template.yaml"
VALID_INSTANCE = REPO_ROOT / "herramientas" / "linkml" / "assets" / "instance-valid.yaml"
INVALID_INSTANCE = REPO_ROOT / "herramientas" / "linkml" / "assets" / "instance-invalid.yaml"


def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATE_CYCLE)] + args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_venv_inexistente_exit_input():
    """--venv-dir inexistente → EXIT_INPUT (2)."""
    result = run_cmd([
        "--venv-dir", "/tmp/no-existe-este-venv",
        "--schema", str(SCHEMA),
        "--target-class", "Catalog",
        "--data", str(VALID_INSTANCE),
    ])
    assert result.returncode == 2, f"Expected exit 2, got {result.returncode}: {result.stderr}"
    assert "ruta especificada" in result.stderr or "no encontrado en la ruta" in result.stderr


def test_linkml_no_ejecutable_exit_perm(tmp_path):
    """Binario linkml sin permiso de ejecución → EXIT_PERM (4)."""
    fake_linkml = tmp_path / "fake-linkml"
    fake_linkml.write_text("#!/bin/sh\necho fake")
    fake_linkml.chmod(0o644)  # sin execute bit

    result = run_cmd([
        "--linkml", str(fake_linkml),
        "--schema", str(SCHEMA),
        "--target-class", "Catalog",
        "--data", str(VALID_INSTANCE),
    ])
    assert result.returncode == 4, f"Expected exit 4, got {result.returncode}: {result.stderr}"
    assert "no ejecutable" in result.stderr or "permiso" in result.stderr.lower()


def test_schema_inexistente_exit_input():
    """Schema no existe → EXIT_INPUT (2)."""
    result = run_cmd([
        "--linkml", str(LINKML_BIN),
        "--schema", "/tmp/no-existe-schema.yaml",
        "--target-class", "Catalog",
        "--data", str(VALID_INSTANCE),
    ])
    assert result.returncode == 2, f"Expected exit 2, got {result.returncode}: {result.stderr}"
    assert "no encontrado" in result.stderr


def test_data_inexistente_exit_input():
    """Fichero de datos no existe → EXIT_INPUT (2)."""
    result = run_cmd([
        "--linkml", str(LINKML_BIN),
        "--schema", str(SCHEMA),
        "--target-class", "Catalog",
        "--data", "/tmp/no-existe-data.yaml",
    ])
    assert result.returncode == 2, f"Expected exit 2, got {result.returncode}: {result.stderr}"
    assert "no encontrado" in result.stderr


@pytest.mark.skipif(LINKML_BIN is None, reason="linkml no disponible en este host")
def test_ciclo_completo_pass():
    """Ciclo completo con fixtures válidas → PASS (exit 0)."""
    result = run_cmd([
        "--linkml", str(LINKML_BIN),
        "--schema", str(SCHEMA),
        "--target-class", "Catalog",
        "--data", str(VALID_INSTANCE), str(INVALID_INSTANCE),
    ])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Verdict: PASS" in result.stdout


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
