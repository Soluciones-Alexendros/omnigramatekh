# Makefile — omnigramatekh
# Gates locales del repo. Todo target debe poder fallar: sin `|| true`.

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

# Rutas relativas al repo: nada depende del HOME del operador.
PROJECT_ROOT := $(shell pwd)
CHECK_STRUCTURE := bash scripts/check-structure.sh

.DEFAULT_GOAL := help

.PHONY: help setup test lint lint-fix validate validate-structure validate-linkml validate-docs validate-links clean

help:
	@echo "Targets disponibles:"
	@echo "  make setup             - Prepara un clon nuevo (npm ci + hooks de Husky)"
	@echo "  make test              - Tests locales (npm test: checks T01–T09 del sitio)"
	@echo "  make lint              - Formato Prettier (falla si hay diferencias)"
	@echo "  make lint-fix          - Reescribe el formato con Prettier"
	@echo "  make validate          - Gate completo: lint + test + estructura"
	@echo "  make validate-structure- Estructura P1 (scripts/check-structure.sh, perfil P1)"
	@echo "  make validate-linkml   - Smoke de las herramientas LinkML"
	@echo "  make validate-docs     - Formato de la documentación"
	@echo "  make validate-links    - Enlaces relativos de la documentación"
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
	.venv/bin/ruff check sitio/pruebas/run_checks.py scripts/check_links.py scripts/_common.py herramientas/linkml/scripts/validate_cycle.py herramientas/linkml/scripts/linkml_env.py --line-length 100 --target-version py311 --select E,F,W,B,UP,S,SIM --ignore E501

lint-fix:
	npx prettier --write .
	.venv/bin/ruff check sitio/pruebas/run_checks.py scripts/check_links.py scripts/_common.py herramientas/linkml/scripts/validate_cycle.py herramientas/linkml/scripts/linkml_env.py --line-length 100 --target-version py311 --select E,F,W,B,UP,S,SIM --ignore E501 --fix
	.venv/bin/ruff format sitio/pruebas/run_checks.py scripts/check_links.py scripts/_common.py herramientas/linkml/scripts/validate_cycle.py herramientas/linkml/scripts/linkml_env.py

validate: lint test validate-structure validate-linkml validate-docs validate-links
	@echo "✅ Gate completo OK (lint + test + estructura P1 + smoke LinkML + docs + enlaces)"

validate-structure:
	@$(CHECK_STRUCTURE) . --profile P1

validate-linkml:
	@bash herramientas/linkml/scripts/tests/smoke_sh.sh

validate-docs:
	npx prettier --check "documentacion/**/*.md" "docs/**/*.md" \
		README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md AGENTS.md ARCHITECTURE.md CODE_OF_CONDUCT.md

validate-links:
	python3 scripts/check_links.py

# Solo cachés y residuos regenerables. Los diagramas de .archify/ son
# entregables versionados: no se tocan aquí.
clean:
	@echo "🧹 Limpiando cachés..."
	rm -rf node_modules/.cache
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f sitio/pruebas/evidencia/run-*.json
	@echo "✅ Limpieza completada (entregables intactos)"
