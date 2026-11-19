#!/usr/bin/env python3
"""Tests del wrapper de contenedor LinkML (detección de Docker y contrato).

Usa un `docker` de mentira en PATH: no requiere Docker real ni red.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
WRAPPER = REPO_ROOT / "herramientas" / "linkml" / "scripts" / "validate_cycle_container.sh"

DIGEST = "sha256:37859c05b9ba1242be63f61d599edf4ba3a312d2d1893c067aefb191311b59c8"


def make_fake_docker(tmp: Path, info_ok: bool, run_exit: int = 0) -> Path:
    """Crea un docker falso que registra sus argumentos."""
    bin_dir = tmp / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    log = tmp / "docker-calls.log"
    script = bin_dir / "docker"
    info_body = "exit 0" if info_ok else "exit 1"
    script.write_text(
        "#!/usr/bin/env bash\n"
        f'echo "$@" >> "{log}"\n'
        'case "$1" in\n'
        f"  info) {info_body} ;;\n"
        f"  run) exit {run_exit} ;;\n"
        "  *) exit 0 ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return log


def run_wrapper(env: dict, args: list[str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(WRAPPER)] + (args or []),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


def base_env(tmp: Path) -> dict:
    env = os.environ.copy()
    env["PATH"] = f"{tmp / 'bin'}:{env['PATH']}"
    return env


def test_daemon_inaccesible_exit_3(tmp_path):
    """Sin daemon accesible → exit 3 para permitir fallback al venv."""
    make_fake_docker(tmp_path, info_ok=False)
    r = run_wrapper(base_env(tmp_path))
    assert r.returncode == 3, r.stderr
    assert "fallback a venv" in r.stderr


def test_ciclo_pass_exit_0(tmp_path):
    """Docker operativo y ciclo OK → exit 0."""
    make_fake_docker(tmp_path, info_ok=True, run_exit=0)
    r = run_wrapper(base_env(tmp_path))
    assert r.returncode == 0, r.stderr


def test_ciclo_fail_propaga_1(tmp_path):
    """El exit del ciclo dentro del contenedor se propaga (1)."""
    make_fake_docker(tmp_path, info_ok=True, run_exit=1)
    r = run_wrapper(base_env(tmp_path))
    assert r.returncode == 1, r.stderr


def test_monta_repo_readonly_y_usa_digest(tmp_path):
    """`docker run` monta el repo :ro y la imagen va fijada por digest."""
    log = make_fake_docker(tmp_path, info_ok=True, run_exit=0)
    r = run_wrapper(base_env(tmp_path))
    assert r.returncode == 0, r.stderr
    calls = log.read_text(encoding="utf-8")
    assert "/repo:ro" in calls, calls
    assert DIGEST in calls, calls
    assert "validate_cycle.py" in calls, calls
    assert "--target-class Catalog" in calls, calls


def test_imagen_override_por_entorno(tmp_path):
    """LINKML_IMAGE sustituye la imagen por defecto."""
    log = make_fake_docker(tmp_path, info_ok=True, run_exit=0)
    env = base_env(tmp_path)
    env["LINKML_IMAGE"] = "example.invalid/linkml@sha256:" + "a" * 64
    r = run_wrapper(env)
    assert r.returncode == 0, r.stderr
    assert "example.invalid/linkml" in log.read_text(encoding="utf-8")


def test_opcion_desconocida_exit_2(tmp_path):
    """Opción inválida → exit 2 (input inválido)."""
    make_fake_docker(tmp_path, info_ok=True)
    r = run_wrapper(base_env(tmp_path), ["--nope"])
    assert r.returncode == 2, r.stderr


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
