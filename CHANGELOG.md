# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `scripts/check-structure.sh`: validador P1 vendorizado (antes dependía de la
  ruta absoluta de un skill fuera del repo).
- `sitio/pruebas/test_menu.js`: pruebas de comportamiento del menú de navegación.

### Changed

- `Makefile`: rutas relativas al repo, `validate` ejecuta también el smoke de
  LinkML, `validate-docs` deja de silenciar errores, `clean` ya no borra los
  diagramas de `.archify/`.
- CI: las actions se actualizan a su major vigente y el job de documentación
  deja de ignorar el fallo de Prettier.
- `documentacion/linkml/SPEC-modelo-linkml.md`: alineada con el ADR 0002
  (skill `linkml` en `herramientas/linkml/`, no un ramo `data` de machineroom).
- `docs/README.md`: delimita `docs/` (guías de uso) frente a `documentacion/`
  (ADRs y especificaciones).
- `.archify/`: solo se versionan el artefacto `.html` y su `candidate.json`;
  los recibos y pasos intermedios quedan fuera del control de versiones.

### Fixed

- Fechas de copyright y changelog corregidas a 2026 (el proyecto nace en 2026).
- Job `validate-docs` del CI, que siempre pasaba por un `|| true`.

## [0.2.0] - 2026-11-18

### Added

- Estructura completa de perfil P1 (governance, CI/CD, issues, docs).
- LICENSE (MIT), CHANGELOG.md, SECURITY.md, CONTRIBUTING.md, AGENTS.md,
  ARCHITECTURE.md, Makefile, .env.example.
- CI/CD: GitHub Actions workflow (quality, test, validate-structure, smoke,
  validate-docs), CODEOWNERS, renovate.json, PR template.
- Issue templates: bug.yml, feature.yml.
- Docs structure: docs/architecture, docs/guides, docs/runbooks, docs/README.md.

### Changed

- README.md: añadida sección «Propósito de este documento».
- Meta-sección «Propósito de este documento» en AGENTS.md, ARCHITECTURE.md,
  SECURITY.md, CONTRIBUTING.md y docs/README.md.

## [0.1.0] - 2026-11-13

### Added

- Sitio estático experimental en `sitio/` (ADR 0001).
- Herramientas LinkML en `herramientas/linkml/` (ADR 0002).
- Documentación en `documentacion/`: ADRs y especificación del modelo.
- Diagramas Archify en `.archify/`.
- Configuración base: package.json, .gitignore, .prettierrc, .lintstagedrc,
  husky.
