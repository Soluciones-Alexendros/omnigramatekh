# Tasks: Estructura P1 — omnigramatekh

> **Estado: completado y publicado en v0.2.0** (2026-11-18).
> Verificado con `scripts/check-structure.sh . --profile P1` → OK, CI 5/5 y
> `make validate`. Los checkpoints finales quedan registrados abajo.

## Module: governance (8 files)

- [x] Task: Crear LICENSE (MIT)
  - Acceptance: Archivo LICENSE en raíz con licencia MIT, copyright "Soluciones-Alexendros"
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "LICENSE"`
  - Files: LICENSE

- [x] Task: Crear CHANGELOG.md (Keep a Changelog)
  - Acceptance: CHANGELOG.md con formato Keep a Changelog, sección "## [Unreleased]" y entrada inicial v0.1.0
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "CHANGELOG"`
  - Files: CHANGELOG.md

- [x] Task: Crear SECURITY.md
  - Acceptance: SECURITY.md con política de seguridad, reporte de vulnerabilidades, versiones soportadas
  - Implementation roles: role-linux, role-back
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "SECURITY"`
  - Files: SECURITY.md

- [x] Task: Crear CONTRIBUTING.md
  - Acceptance: CONTRIBUTING.md con guía de contribución, code of conduct ref, proceso PR, tests
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "CONTRIBUTING"`
  - Files: CONTRIBUTING.md

- [x] Task: Crear AGENTS.md (basado en operador)
  - Acceptance: AGENTS.md adaptado del AGENTS.md del operador (~/.pi/agent/AGENTS.md) para el repo
  - Implementation roles: role-back
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "AGENTS"`
  - Files: AGENTS.md

- [x] Task: Crear ARCHITECTURE.md (arquitectura actual)
  - Acceptance: ARCHITECTURE.md describiendo arquitectura actual: sitio estático (sitio/), herramientas LinkML (herramientas/linkml/), documentación (documentacion/), diagramas (.archify/)
  - Implementation roles: role-back
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "ARCHITECTURE"`
  - Files: ARCHITECTURE.md

- [x] Task: Crear Makefile (targets estándar + proyecto)
  - Acceptance: Makefile con targets: test, lint, validate, clean, linkml-validate, docs-build, help
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh, `make help`
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "Makefile"` && `make help`
  - Files: Makefile

- [x] Task: Crear .env.example
  - Acceptance: .env.example con variables de ejemplo (vacías) para entorno de desarrollo
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "env.example"`
  - Files: .env.example

**Checkpoint CP1**: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` → solo faltan ci-cd, issues, docs-structure, readme-fix

---

## Module: ci-cd (4 files)

- [x] Task: Crear .github/workflows/ci.yml
  - Acceptance: Workflow CI con jobs: lint (prettier, markdownlint), test (npm test), validate (check-product-structure.sh), runs on push/PR to main
  - Implementation roles: role-linux, role-back
  - Test surfaces: actionlint, CI execution
  - Verify: `actionlint .github/workflows/ci.yml` && `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "ci.yml"`
  - Files: .github/workflows/ci.yml

- [x] Task: Crear .github/CODEOWNERS (@alexendros)
  - Acceptance: CODEOWNERS con `@alexendros` como owner de todo el repo
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "CODEOWNERS"`
  - Files: .github/CODEOWNERS

- [x] Task: Crear .github/renovate.json
  - Acceptance: renovate.json con config agrupada: npm dependencies, GitHub Actions, docker (si aplica), automerge en patch/minor
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "renovate"`
  - Files: .github/renovate.json

- [x] Task: Crear .github/PULL_REQUEST_TEMPLATE.md
  - Acceptance: PR template con checklist: description, testing, docs, breaking changes, linked issues
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "PULL_REQUEST_TEMPLATE"`
  - Files: .github/PULL_REQUEST_TEMPLATE.md

**Checkpoint CP2**: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` → solo faltan docs-structure, readme-fix

---

## Module: issues (2 files)

- [x] Task: Crear .github/ISSUE_TEMPLATE/bug.yml
  - Acceptance: Plantilla bug con campos: description, steps, expected, actual, environment, logs
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "bug.yml"`
  - Files: .github/ISSUE_TEMPLATE/bug.yml

- [x] Task: Crear .github/ISSUE_TEMPLATE/feature.yml
  - Acceptance: Plantilla feature con campos: problem, solution, alternatives, acceptance criteria, breaking changes
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "feature.yml"`
  - Files: .github/ISSUE_TEMPLATE/feature.yml

---

## Module: docs-structure (5 items)

- [x] Task: Crear directorios docs/architecture, docs/guides, docs/runbooks
  - Acceptance: Tres directorios creados bajo docs/
  - Implementation roles: role-linux
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "docs/"`
  - Files: docs/architecture/, docs/guides/, docs/runbooks/

- [x] Task: Crear docs/README.md
  - Acceptance: docs/README.md con índice de navegación a architecture/, guides/, runbooks/
  - Implementation roles: role-linux, role-clean-code
  - Test surfaces: check-product-structure.sh
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh . | grep -c "docs/README"`
  - Files: docs/README.md

**Checkpoint CP3**: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` → solo falta readme-fix

---

## Module: readme-fix (1 file)

- [x] Task: Añadir "### Propósito de este documento" a README.md
  - Acceptance: README.md incluye sección `### Propósito de este documento` tras el título principal
  - Implementation roles: role-clean-code
  - Test surfaces: check-product-structure.sh, prettier
  - Verify: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` (exit 0) && `npx prettier --check README.md`
  - Files: README.md

---

## Final Checkpoints

- [x] **CP4**: `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` → **Exit 0, 0 errores P1**
- [x] **CP5**: `actionlint .github/workflows/ci.yml` → Sin errores
- [x] **CP6**: `npx prettier --check .` → Pasa
- [x] **CP7**: `npm test` → Pasa (no regresiones)
