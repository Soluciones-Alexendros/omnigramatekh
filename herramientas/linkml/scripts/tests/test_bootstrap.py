#!/usr/bin/env python3
"""Tests de bootstrap_arch.sh — deterministas en cualquier host.

Simula la distro con BOOTSTRAP_OS_RELEASE y un `pacman` de mentira, así que no
depende de estar en Arch ni de tener Docker. Verifica el contrato real:
- Arch + dry-run → plan y exit 0; --dry-run gana siempre sobre --apply.
- Distro no soportada → exit 2 con mensaje explícito.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BOOTSTRAP = REPO_ROOT / "herramientas" / "linkml" / "scripts" / "bootstrap_arch.sh"


def fake_bin(tmp: Path) -> Path:
    """Crea un `pacman` falso que simula paquetes instalados."""
    bin_dir = tmp / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    pacman = bin_dir / "pacman"
    pacman.write_text(
        "#!/usr/bin/env bash\n"
        'case "$1" in\n'
        "  -Q) exit 0 ;;\n"  # python y python-pip "instalados"
        "  *) exit 0 ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    pacman.chmod(0o755)
    return bin_dir


def write_os_release(tmp: Path, name: str, body: str) -> Path:
    f = tmp / name
    f.write_text(body, encoding="utf-8")
    return f


def run_bootstrap(tmp: Path, os_release: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PATH"] = f"{fake_bin(tmp)}:{env['PATH']}"
    env["BOOTSTRAP_OS_RELEASE"] = str(os_release)
    return subprocess.run(
        ["bash", str(BOOTSTRAP)] + args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )


def arch_release(tmp: Path) -> Path:
    return write_os_release(tmp, "os-release-arch", 'ID=arch\nID_LIKE=archlinux\n')


def ubuntu_release(tmp: Path) -> Path:
    return write_os_release(tmp, "os-release-ubuntu", 'ID=ubuntu\nID_LIKE=debian\n')


def test_arch_dry_run_default(tmp_path):
    """Arch + sin flags → dry-run con plan, exit 0."""
    r = run_bootstrap(tmp_path, arch_release(tmp_path), [])
    assert r.returncode == 0, r.stderr
    assert "Dry-run: nada ejecutado" in r.stdout


def test_arch_dry_run_explicito(tmp_path):
    """Arch + --dry-run → dry-run, exit 0."""
    r = run_bootstrap(tmp_path, arch_release(tmp_path), ["--dry-run"])
    assert r.returncode == 0, r.stderr
    assert "Dry-run: nada ejecutado" in r.stdout


def test_dry_run_gana_sobre_apply_ambos_ordenes(tmp_path):
    """--dry-run gana sobre --apply en los dos órdenes (no depende del orden)."""
    osr = arch_release(tmp_path)
    for args in (["--dry-run", "--apply"], ["--apply", "--dry-run"]):
        r = run_bootstrap(tmp_path, osr, args)
        assert r.returncode == 0, f"{args}: {r.stderr}"
        assert "Dry-run: nada ejecutado" in r.stdout, f"{args} no hizo dry-run"


def test_distro_no_soportada_exit_2(tmp_path):
    """Distro no Arch → exit 2 con el motivo (y sin tocar nada)."""
    r = run_bootstrap(tmp_path, ubuntu_release(tmp_path), [])
    assert r.returncode == 2, r.stderr
    assert "solo soporta Arch" in r.stderr


def test_flag_desconocida_exit_2(tmp_path):
    """Flag desconocida → exit 2."""
    r = run_bootstrap(tmp_path, arch_release(tmp_path), ["--flag-inexistente"])
    assert r.returncode == 2, r.stderr


def test_help_exit_0(tmp_path):
    """--help → exit 0 con la ayuda."""
    r = run_bootstrap(tmp_path, arch_release(tmp_path), ["--help"])
    assert r.returncode == 0, r.stderr
    assert "Uso:" in r.stdout


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
