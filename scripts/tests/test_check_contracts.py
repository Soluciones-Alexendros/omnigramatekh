#!/usr/bin/env python3
"""Tests de scripts/check_contracts.py — un caso negativo por contrato (C1–C5).

Cada test construye un repo mínimo en tmp_path: así el gate se prueba contra el
fallo real, no contra el repo sano.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "check_contracts.py"

PINNED = "a" * 40
CI_OK = f"""name: CI
on:
  push:
    branches: [main]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@{PINNED} # v7
        with:
          persist-credentials: false
      - run: npm test
"""


def make_repo(tmp: Path, *, version="0.1.0", changelog=None, readme="", ci=CI_OK, docs_ok=True) -> Path:
    root = tmp / "repo"
    (root / "docs" / "guides").mkdir(parents=True)
    (root / ".github" / "workflows").mkdir(parents=True)

    (root / "package.json").write_text(json.dumps({"name": "x", "version": version}), encoding="utf-8")
    (root / "CHANGELOG.md").write_text(
        changelog if changelog is not None else f"# Changelog\n\n## [Unreleased]\n\n## [{version}] - 2026-01-01\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text(readme, encoding="utf-8")
    (root / ".github" / "workflows" / "ci.yml").write_text(ci, encoding="utf-8")

    docs_readme = "# Docs\n\n| Dir | Contenido |\n|---|---|\n| [guides/](guides/) | guías |\n"
    (root / "docs" / "README.md").write_text(docs_readme, encoding="utf-8")
    guide = root / "docs" / "guides" / ("guia.md" if docs_ok else ".gitkeep")
    guide.write_text("contenido\n", encoding="utf-8")
    return root


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root)],
        capture_output=True,
        text=True,
    )


def test_repo_sano_pasa(tmp_path):
    r = run(make_repo(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr


def test_c1_version_no_coincide(tmp_path):
    root = make_repo(tmp_path, version="0.2.0", changelog="# Changelog\n\n## [0.1.0] - 2026-01-01\n")
    r = run(root)
    assert r.returncode == 1
    assert "C1" in r.stderr


def test_c1_changelog_sin_entradas(tmp_path):
    root = make_repo(tmp_path, changelog="# Changelog\n\n## [Unreleased]\n")
    r = run(root)
    assert r.returncode == 1
    assert "C1" in r.stderr


def test_c2_readme_version_incoherente(tmp_path):
    root = make_repo(tmp_path, version="0.1.0", readme="# X\n\nVersión **9.9.9** lista.\n")
    r = run(root)
    assert r.returncode == 1
    assert "C2" in r.stderr


def test_c3_job_vacio(tmp_path):
    ci = """name: CI
on:
  push:
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - run: "true"
"""
    root = make_repo(tmp_path, ci=ci)
    r = run(root)
    assert r.returncode == 1
    assert "C3" in r.stderr


def test_c4_docs_vacio_solo_gitkeep(tmp_path):
    root = make_repo(tmp_path, docs_ok=False)
    r = run(root)
    assert r.returncode == 1
    assert "C4" in r.stderr


def test_c5_uses_sin_sha(tmp_path):
    ci = CI_OK.replace(f"actions/checkout@{PINNED}", "actions/checkout@v7")
    root = make_repo(tmp_path, ci=ci)
    r = run(root)
    assert r.returncode == 1
    assert "C5" in r.stderr


def test_no_confunde_on_con_jobs(tmp_path):
    """`on:` tiene claves de 2 espacios; no deben contarse como jobs."""
    root = make_repo(tmp_path)
    r = run(root)
    assert r.returncode == 0, r.stderr
    assert "push" not in r.stdout


def test_root_inexistente_exit_2(tmp_path):
    r = run(tmp_path / "no-existe")
    assert r.returncode == 2


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
