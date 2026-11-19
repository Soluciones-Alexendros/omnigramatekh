#!/usr/bin/env python3
"""Tests pytest para linkml_env.py - caminos de error."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LINKML_ENV = REPO_ROOT / "herramientas" / "linkml" / "scripts" / "linkml_env.py"
LINKML_BIN = REPO_ROOT / ".venv" / "bin" / "linkml"


def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINKML_ENV)] + args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_venv_inexistente_exit_input():
    """--venv-dir inexistente → EXIT_INPUT (2)."""
    result = run_cmd(["--venv-dir", "/tmp/no-existe-este-venv"])
    assert result.returncode == 2, f"Expected exit 2, got {result.returncode}: {result.stderr}"
    output = result.stdout + result.stderr
    assert "ruta especificada" in output or "no encontrado en la ruta" in output


def test_linkml_no_ejecutable_exit_perm(tmp_path):
    """Binario linkml sin permiso de ejecución → EXIT_PERM (4)."""
    fake_linkml = tmp_path / "fake-linkml"
    fake_linkml.write_text("#!/bin/sh\necho fake")
    fake_linkml.chmod(0o644)

    result = run_cmd(["--linkml", str(fake_linkml)])
    assert result.returncode == 4, f"Expected exit 4, got {result.returncode}: {result.stderr}"
    output = result.stdout + result.stderr
    assert "no ejecutable" in output or "permiso" in output.lower()


def test_linkml_no_encontrado_exit_missing():
    """Sin args y sin linkml en PATH → EXIT_MISSING (3)."""
    # Use a clean PATH without linkml
    env = {"PATH": "/usr/bin:/bin"}  # minimal PATH
    result = subprocess.run(
        [sys.executable, str(LINKML_ENV)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )
    assert result.returncode == 3, f"Expected exit 3, got {result.returncode}: {result.stderr}"
    output = result.stdout + result.stderr
    assert "no encontrado" in output.lower()


def test_preflight_pass():
    """Pre-flight con linkml válido → PASS (exit 0)."""
    result = run_cmd(["--linkml", str(LINKML_BIN)])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Verdict: PASS" in result.stdout


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
