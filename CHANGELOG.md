# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_(sin cambios pendientes)_

## [0.3.0] - 2026-11-19

Remediación de la auditoría crítica y cierre de las cinco mejoras propuestas.

### Added

- Gates en navegador real (Chromium): accesibilidad con **contraste efectivo**,
  reflow WCAG 1.4.10 a 320 px y presupuestos de rendimiento con Lighthouse CI.
- Ciclo LinkML en contenedor OCI fijado por digest, con fallback al venv local.
- Gates de **contrato** (`scripts/check_contracts.py`): versión coherente con
  CHANGELOG y README, jobs de CI que ejecutan algo real, `docs/` con contenido,
  y todo `uses:` fijado por SHA.
- Seguridad de pipeline: `zizmor` + `actionlint` como gate con versiones fijadas
  y OpenSSF Scorecard semanal con SARIF a code scanning.
- Suite de validadores: 42 tests (LinkML, contratos, módulo común), con caminos
  de error y skips limpios donde falta el binario.
- `shellcheck` en `make lint` y CI, con versión fijada.

### Changed

- `make validate` incorpora contratos; `make validate-workflows` audita workflows.
- `validate_cycle.py`/`linkml_env.py` comparten `scripts/_common.py` (sin duplicar
  `find_linkml`, `run` ni los exit codes).
- Lock de LinkML generado para Python 3.12 con `--require-hashes`.

### Fixed

- Secrets gate: T01/T06 detectan claves reales por forma (no por subcadena) y no
  registran el valor del secreto (hallazgo CodeQL).
- `--venv-dir` inexistente ya no cae en silencio a otro `linkml`; devuelve error.
- `--dry-run` gana siempre sobre `--apply` en el bootstrap de LinkML.
- `check_links.py`: argumento inexistente → exit 2; enlaces fuera del repo → fallo.
- Accesibilidad: si faltan `jsdom`/`axe-core`, el gate falla en CI (antes pasaba).
- 8 checkouts de Actions persistían credenciales (`persist-credentials: false`).

### Removed

- T08 (test tautológico que comprobaba `shutil.copy2` y mutaba `index.html`).
- Dos generaciones superadas de `.archify/` (~48.000 líneas).

## [0.2.1] - 2026-11-18

### Added

- `scripts/check-structure.sh`: validador P1 vendorizado (antes dependía de la
  ruta absoluta de un skill fuera del repo).
- `sitio/pruebas/test_menu.js`: pruebas de comportamiento del menú de navegación.
- `sitio/pruebas/test_a11y.js`: T04 pasa a ser automática con axe-core (WCAG 2.1
  AA) sobre el HTML real; una violación rompe el gate.
- `documentacion/linkml/MAPEO-entidades.md`: LinkML canónico ↔ SQL de proyección.
- `axe-core` y `jsdom` como devDependencies del gate de accesibilidad.

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
- `sitio/pruebas/run_checks.py`: el gate separa lo bloqueante de lo no
  verificado; T04 deja de reportarse aquí porque la cubre `test_a11y.js`.
- `renovate.json`: sin automerge; toda actualización pasa por revisión.

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
