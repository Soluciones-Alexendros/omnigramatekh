# Makefile — omnigramatekh
# Gates locales del repo. Todo target debe poder fallar: sin `|| true`.

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

# Rutas relativas al repo: nada depende del HOME del operador.
PROJECT_ROOT := $(shell pwd)
CHECK_STRUCTURE := bash scripts/check-structure.sh

.DEFAULT_GOAL := help

.PHONY: help setup test test-browser lint lint-fix validate validate-structure validate-linkml validate-docs validate-links validate-workflows clean

help:
	@echo "Targets disponibles:"
	@echo "  make setup             - Prepara un clon nuevo (npm ci + hooks de Husky)"
	@echo "  make test              - Tests locales (npm test: checks T01–T09 del sitio)"
	@echo "  make test-browser      - Gates en Chromium (a11y+contraste, reflow, Lighthouse)"
	@echo "  make lint              - Formato Prettier (falla si hay diferencias)"
	@echo "  make lint-fix          - Reescribe el formato con Prettier"
	@echo "  make validate          - Gate completo: lint + test + estructura"
	@echo "  make validate-structure- Estructura P1 (scripts/check-structure.sh, perfil P1)"
	@echo "  make validate-linkml   - Smoke de las herramientas LinkML"
	@echo "  make validate-docs     - Formato de la documentación"
	@echo "  make validate-links    - Enlaces relativos de la documentación"
	@echo "  make validate-workflows- actionlint + zizmor sobre .github/workflows"
	@echo "  make clean             - Limpia cachés locales (no borra entregables)"

# Preparación de un clon nuevo: dependencias exactas del lockfile + hooks. 
setup:
	npm ci
	@echo "✅ Entorno listo (node $(shell node -v))"

# Tests: exit 1 si alguna prueba T01–T09 falla; informa de las manuales.
test:
	npm test

lint:
	npx prettier --check .
	.venv/bin/ruff check .

lint-fix:
	npx prettier --write .
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

validate: lint test validate-structure validate-linkml validate-docs validate-links
	@echo "✅ Gate completo OK (lint + test + estructura P1 + smoke LinkML + docs + enlaces)"

# Gates en navegador real (Chromium): accesibilidad con contraste, reflow y
# presupuestos de rendimiento. Requiere `npx playwright install chromium`.
test-browser:
	npm run test:browser

validate-structure:
	@$(CHECK_STRUCTURE) . --profile P1

# Prefiere contenedor OCI (reproducible, sin tocar el host). Si Docker no está
# disponible (exit 3), cae al venv local vía smoke_sh.sh.
validate-linkml:
	@set +e; bash herramientas/linkml/scripts/validate_cycle_container.sh; rc=$$?; \
	  if [ $$rc -eq 3 ]; then bash herramientas/linkml/scripts/tests/smoke_sh.sh; \
	  else exit $$rc; fi

validate-docs:
	npx prettier --check "documentacion/**/*.md" "docs/**/*.md" \
		README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md AGENTS.md ARCHITECTURE.md CODE_OF_CONDUCT.md

validate-links:
	python3 scripts/check_links.py

# Endurecimiento de workflows: sintaxis (actionlint) y auditoría de seguridad
# (zizmor). Requiere actionlint y zizmor en PATH.
validate-workflows:
	@command -v actionlint >/dev/null 2>&1 || { echo "falta actionlint" >&2; exit 3; }
	@command -v zizmor >/dev/null 2>&1 || { echo "falta zizmor" >&2; exit 3; }
	actionlint .github/workflows/*.yml
	zizmor --persona=regular .github/workflows/

# Solo cachés y residuos regenerables. Los diagramas de .archify/ son
# entregables versionados: no se tocan aquí.
clean:
	@echo "🧹 Limpiando cachés..."
	rm -rf node_modules/.cache
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f sitio/pruebas/evidencia/run-*.json
	@echo "✅ Limpieza completada (entregables intactos)"
