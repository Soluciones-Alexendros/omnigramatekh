#!/usr/bin/env python3
"""Tests directos de scripts/_common.py (sin subprocess).

Importar el módulo (en vez de lanzar los scripts) es lo que permite medir
cobertura real y ejecutar pruebas de mutación sobre sus ramas.
"""

import stat
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import _common  # noqa: E402


def make_executable(path: Path, content: str = "#!/bin/sh\nexit 0\n") -> Path:
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


# --- find_linkml -----------------------------------------------------------


def test_find_linkml_explicito_existente(tmp_path):
    binary = make_executable(tmp_path / "linkml")
    assert _common.find_linkml(str(binary), None) == str(binary)


def test_find_linkml_explicito_inexistente_no_cae_a_path(tmp_path, monkeypatch):
    monkeypatch.setattr(_common.shutil, "which", lambda _: "/usr/bin/linkml")
    assert _common.find_linkml(str(tmp_path / "no-existe"), None) is None


def test_find_linkml_venv_dir_con_binario(tmp_path):
    binary = make_executable(tmp_path / "bin" / "linkml") if (tmp_path / "bin").mkdir() is None else None
    assert _common.find_linkml(None, str(tmp_path)) == str(binary)


def test_find_linkml_venv_dir_sin_binario_no_cae_a_path(tmp_path, monkeypatch):
    monkeypatch.setattr(_common.shutil, "which", lambda _: "/usr/bin/linkml")
    assert _common.find_linkml(None, str(tmp_path)) is None


def test_find_linkml_sin_argumentos_usa_path(monkeypatch):
    monkeypatch.setattr(_common.shutil, "which", lambda _: "/usr/bin/linkml")
    assert _common.find_linkml(None, None) == "/usr/bin/linkml"


# --- verify_executable -----------------------------------------------------


def test_verify_executable_ok(tmp_path):
    binary = make_executable(tmp_path / "tool")
    assert _common.verify_executable(str(binary)) == (True, "ok")


def test_verify_executable_inexistente(tmp_path):
    ok, detail = _common.verify_executable(str(tmp_path / "no-existe"))
    assert ok is False and "no existe" in detail


def test_verify_executable_directorio(tmp_path):
    ok, detail = _common.verify_executable(str(tmp_path))
    assert ok is False and "no es un fichero" in detail


def test_verify_executable_sin_bit_de_ejecucion(tmp_path):
    binary = tmp_path / "tool"
    binary.write_text("#!/bin/sh\n", encoding="utf-8")
    binary.chmod(0o644)
    ok, detail = _common.verify_executable(str(binary))
    assert ok is False and "no ejecutable" in detail


# --- run ------------------------------------------------------------------


def test_run_captura_salida_y_codigo():
    result = _common.run([sys.executable, "-c", "import sys; print('hola'); sys.exit(3)"])
    assert result["exit_code"] == 3
    assert result["stdout"] == "hola"


def test_run_oserror_devuelve_exit_perm(monkeypatch):
    def boom(*_args, **_kwargs):
        raise PermissionError(13, "denied")

    monkeypatch.setattr(subprocess, "run", boom)
    result = _common.run(["cualquier-cosa"])
    assert result["exit_code"] == _common.EXIT_PERM
    assert "denied" in result["stderr"]


def test_exit_codes_canonicos():
    assert (_common.EXIT_OK, _common.EXIT_ERROR, _common.EXIT_INPUT,
            _common.EXIT_MISSING, _common.EXIT_PERM) == (0, 1, 2, 3, 4)


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
