#!/usr/bin/env bash
# Ciclo LinkML en contenedor OCI (reproducible en cualquier host con Docker).
#
# Ejecuta `validate_cycle.py` DENTRO de la imagen oficial, con el repo montado
# en solo lectura. No instala nada en el host ni toca el Python del sistema.
#
# Exit codes: 0 ciclo PASS · 1 ciclo FAIL · 2 input inválido · 3 sin Docker
#             (el llamador puede hacer fallback al venv) · 4 permiso.
#
# Uso:
#   herramientas/linkml/scripts/validate_cycle_container.sh [--image IMG]
#   LINKML_IMAGE=linkml/linkml@sha256:... validate_cycle_container.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ASSETS="$REPO_ROOT/herramientas/linkml/assets"

# Imagen fijada por digest (manifest list multi-arch de linkml/linkml:1.12.1).
DEFAULT_IMAGE="linkml/linkml@sha256:37859c05b9ba1242be63f61d599edf4ba3a312d2d1893c067aefb191311b59c8"
IMAGE="${LINKML_IMAGE:-$DEFAULT_IMAGE}"

SCHEMA="herramientas/linkml/assets/schema-template.yaml"
DATA=(
  "herramientas/linkml/assets/instance-valid.yaml"
  "herramientas/linkml/assets/instance-invalid.yaml"
)
TARGET_CLASS="Catalog"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image) IMAGE="${2:?--image requiere un valor}"; shift ;;
    --help|-h)
      sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "ERROR: opción desconocida: $1" >&2; exit 2 ;;
  esac
  shift
done

if [[ ! -f "$REPO_ROOT/$SCHEMA" ]]; then
  echo "ERROR: falta el esquema: $SCHEMA" >&2
  exit 2
fi
for d in "${DATA[@]}"; do
  [[ -f "$REPO_ROOT/$d" ]] || { echo "ERROR: falta el dato: $d" >&2; exit 2; }
done

if ! command -v docker >/dev/null 2>&1; then
  echo "container: docker no disponible (fallback a venv)" >&2
  exit 3
fi
# `docker info` falla sin daemon o sin permisos sobre el socket.
if ! docker info >/dev/null 2>&1; then
  echo "container: daemon de Docker inaccesible (fallback a venv)" >&2
  exit 3
fi

echo "container: $IMAGE"
docker run --rm \
  --volume "$REPO_ROOT:/repo:ro" \
  --workdir /repo \
  "$IMAGE" \
  python3 herramientas/linkml/scripts/validate_cycle.py \
    --schema "$SCHEMA" \
    --target-class "$TARGET_CLASS" \
    --data "${DATA[@]}"
