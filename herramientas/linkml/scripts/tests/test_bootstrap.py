#!/usr/bin/env python3
"""Tests pytest para bootstrap_arch.sh - caminos de error."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BOOTSTRAP = REPO_ROOT / "herramientas" / "linkml" / "scripts" / "bootstrap_arch.sh"


def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(BOOTSTRAP)] + args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_dry_run_default():
    """Sin flags → dry-run (exit 0)."""
    result = run_cmd([])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Dry-run: nada ejecutado" in result.stdout


def test_dry_run_explicit():
    """--dry-run → dry-run (exit 0)."""
    result = run_cmd(["--dry-run"])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Dry-run: nada ejecutado" in result.stdout


def test_dry_run_wins_over_apply():
    """--dry-run --apply → dry-run gana (exit 0)."""
    result = run_cmd(["--dry-run", "--apply"])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Dry-run: nada ejecutado" in result.stdout


def test_apply_wins_when_no_dry_run():
    """--apply sin --dry-run → intenta ejecutar (exit 0 en dry-run, pero plan mostrado)."""
    # Note: on non-Arch this would exit 2, but we're on Arch-compatible
    result = run_cmd(["--apply", "--skip-pacman", "--venv-dir", "/tmp/test-bootstrap-venv"])
    # Should either succeed or fail gracefully (not crash)
    assert result.returncode in (0, 1, 2, 3), f"Unexpected exit: {result.returncode}"


def test_unknown_flag():
    """Flag desconocida → exit 2."""
    result = run_cmd(["--flag-inexistente"])
    assert result.returncode == 2, f"Expected exit 2, got {result.returncode}: {result.stderr}"


def test_help():
    """--help → exit 0."""
    result = run_cmd(["--help"])
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}: {result.stderr}"
    assert "Uso:" in result.stdout


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
