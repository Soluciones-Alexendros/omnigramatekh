#!/usr/bin/env bash
# Smoke para scripts de data-linkml: --help (exit 0) + py_compile de cada .py,
# y dry-run del bootstrap (sin sudo, sin red, sin efectos secundarios).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

fail=0
ok() { echo "OK: $1"; }
bad() { echo "FALLO: $1" >&2; fail=1; }

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

if [[ -f "$SCRIPT_DIR/bootstrap_arch.sh" ]]; then
  # bootstrap_arch.sh es específico de Arch y derivadas (Omarchy, Manjaro...):
  # se acepta ID o ID_LIKE. En otras distribuciones el dry-run se omite.
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

if [[ $fail -eq 0 ]]; then
  echo "smoke herramientas/linkml: VERDE"
else
  echo "smoke herramientas/linkml: ROJO" >&2
fi
exit "$fail"
