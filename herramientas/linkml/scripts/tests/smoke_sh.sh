#!/usr/bin/env bash
# Smoke para scripts de data-linkml:
# 1) --help (exit 0) + py_compile de cada .py
# 2) dry-run del bootstrap (sin sudo, sin red, sin efectos secundarios)
# 3) ciclo real validate_cycle.py sobre fixtures (si linkml está disponible)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS_DIR="$SCRIPT_DIR/../assets"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

fail=0
ok() { echo "OK: $1"; }
bad() { echo "FALLO: $1" >&2; fail=1; }

# 1) --help + py_compile para cada script .py
shopt -s nullglob
count=0
for py in "$SCRIPT_DIR"/*.py; do
  count=$((count + 1))
  base="$(basename "$py")"
  if python3 "$py" --help >/dev/null 2>&1; then
    ok "--help $base exit 0"
  else
    bad "--help $base exit $?"
  fi
  if python3 -m py_compile "$py"; then
    ok "py_compile $base"
  else
    bad "py_compile $base"
  fi
done
shopt -u nullglob

if [[ $count -eq 0 ]]; then
  bad "sin scripts .py en $SCRIPT_DIR"
fi

# 2) bootstrap_arch.sh --dry-run (solo en Arch/derivadas)
if [[ -f "$SCRIPT_DIR/bootstrap_arch.sh" ]]; then
  OS_ID="$(grep -E '^ID=' /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '"' || echo unknown)"
  OS_LIKE="$(grep -E '^ID_LIKE=' /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '"' || echo '')"
  is_arch=0
  for cand in $OS_ID $OS_LIKE; do
    [[ "$cand" == "arch" || "$cand" == "archlinux" ]] && is_arch=1
  done
  if [[ "$is_arch" -eq 1 ]]; then
    if bash "$SCRIPT_DIR/bootstrap_arch.sh" --dry-run >/dev/null 2>&1; then
      ok "bootstrap_arch.sh --dry-run exit 0"
    else
      bad "bootstrap_arch.sh --dry-run exit $?"
    fi
  else
    ok "bootstrap_arch.sh --dry-run omitido (sistema no-Arch: $OS_ID)"
  fi
else
  bad "falta bootstrap_arch.sh"
fi

# 3) Ciclo real validate_cycle.py sobre fixtures (si linkml disponible)
LINKML_BIN=""
if [[ -x "$REPO_ROOT/.venv/bin/linkml" ]]; then
  LINKML_BIN="$REPO_ROOT/.venv/bin/linkml"
elif command -v linkml >/dev/null 2>&1; then
  LINKML_BIN="$(command -v linkml)"
fi

if [[ -n "$LINKML_BIN" ]]; then
  echo "Ejecutando validate_cycle.py con linkml: $LINKML_BIN"
  if python3 "$SCRIPT_DIR/validate_cycle.py" \
      --linkml "$LINKML_BIN" \
      --schema "$ASSETS_DIR/schema-template.yaml" \
      --target-class Catalog \
      --data "$ASSETS_DIR/instance-valid.yaml" "$ASSETS_DIR/instance-invalid.yaml" >/dev/null 2>&1
  then
    ok "validate_cycle.py ciclo completo (L1-L4) PASS"
  else
    bad "validate_cycle.py ciclo completo FAIL (exit $?)"
  fi
else
  ok "validate_cycle.py omitido (linkml no disponible en PATH/venv)"
fi

if [[ $fail -eq 0 ]]; then
  echo "smoke herramientas/linkml: VERDE"
else
  echo "smoke herramientas/linkml: ROJO" >&2
fi
exit "$fail"