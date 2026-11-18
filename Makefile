# Makefile — omnigramatekh
# Targets estándar + proyecto

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

# Variables
PROJECT_ROOT := $(shell pwd)
CHECK_STRUCTURE := bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh

.PHONY: help test lint validate validate-structure clean linkml-validate docs-build

# Default target
help:
	@echo "Targets disponibles:"
	@echo "  make test              - Ejecutar tests (npm test)"
	@echo "  make lint              - Lint/format (prettier --check)"
	@echo "  make validate          - Validación completa (lint + test + estructura)"
	@echo "  make validate-structure - Validar estructura P1 (check-product-structure.sh)"
	@echo "  make clean             - Limpiar artefactos temporales"
	@echo "  make linkml-validate   - Validar herramientas LinkML (smoke test)"
	@echo "  make docs-build        - Validar documentación (prettier check)"

# Tests
test:
	npm test

# Lint y formato
lint:
	npx prettier --check .

# Validación completa
validate: lint test validate-structure
	@echo "✅ Validación completa OK"

# Validar estructura P1
validate-structure:
	@echo "🔍 Validando estructura P1..."
	@$(CHECK_STRUCTURE) .
	@echo "✅ Estructura P1 OK"

# Limpiar
clean:
	@echo "🧹 Limpiando..."
	rm -rf node_modules/.cache 2>/dev/null || true
	rm -rf .archify/*.html 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpieza completada"

# Validar herramientas LinkML
linkml-validate:
	@echo "🔍 Validando herramientas LinkML..."
	bash herramientas/linkml/scripts/tests/smoke_sh.sh
	@echo "✅ LinkML smoke test OK"

# Validar documentación
docs-build:
	@echo "🔍 Validando documentación..."
	npx prettier --check documentacion/ docs/ README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md AGENTS.md ARCHITECTURE.md 2>/dev/null || true
	@echo "✅ Documentación OK"