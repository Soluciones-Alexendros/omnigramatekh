# Implementation Plan: Auditoría Crítica — Remediación omnigramatekh

## Overview

Remediar 21 defectos (19 confirmados, 2 sospechas) de la auditoría crítica en commit `4e3fb83`, organizados en 5 módulos independientes por riesgo/impacto: gates que mienten, robustez LinkML, cadena de suministro, artefactos/docs, higiene. Cada módulo se implementa y verifica independientemente; el gate global `make validate` debe pasar al final.

## Architecture Decisions

- **Módulo común Python:** Extraer `find_linkml`, `run`, `EXIT_*` a `scripts/_common.py` para eliminar duplicación D-012 y fijar contrato de errores.
- **Gates de contenido:** `check-structure.sh` exigirá ≥1 fichero real en `docs/*` (no solo directorios). Alternativa: relajar gate y documentar decisión en `docs/README.md`.
- **`.archify` canon:** Versionar solo `candidate.json` + generar HTML en CI/release; declarar canónica en `.archify/README.md` y borrar 2 generaciones superadas.
- **LinkML en CI:** Job "Validate LinkML Tools" ejecuta `validate_cycle.py` real sobre fixtures; smoke Sh lo invoca.
- **Seguridad pipeline:** `gitleaks` en pre-commit + CI; actions por SHA; lock con hashes; Renovate `pinGitHubActionDigests`.
- **Tests negativos:** Por cada gate modificado, test que rompa algo a propósito y verifique fallo.

## Task List

### Phase 1: gates-truth (D-019, D-018, D-017, D-005, D-001)

- [ ] **Task A1:** T01/T06 — Sustituir detección por subcadena con detectores de forma (regex claves reales) y caso prueba «secretaría»
  - Acceptance: T01/T06 pasan con «La secretaría guarda el secreto»; detectan `AKIA[0-9A-Z]{16}`, `ghp_[a-zA-Z0-9]{36}`, `-----BEGIN.*PRIVATE KEY-----`, `(?i)(api[_-]?key|password|token)\s*[:=]\s*['"]\S{8,}`
  - Verification: `npm run test:sitio` (T01–T09 pass) + test negativo añadiendo secreto real → fail
  - Roles: role-front (sitio/pruebas), role-clean-code (regex limpias)
  - Test surfaces: `run_checks.py::check_T01`, `run_checks.py::check_T06`
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [ ] **Task A2:** T02 — Parsear HTML con `html.parser` / selector por `id`, no `split`
  - Acceptance: T02 pasa independientemente del orden de secciones; test con secciones reordenadas
  - Verification: `npm run test:sitio` + test manual reordenando secciones en copia
  - Roles: role-front, role-clean-code
  - Test surfaces: `run_checks.py::check_T02`
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [ ] **Task A3:** `test_a11y.js` — Catch solo `MODULE_NOT_FOUND`; en CI (`process.env.CI`) convertir skip en fallo
  - Acceptance: jsdom roto → exit 1 en CI; skip solo si módulo no instalado; comentario actualizado
  - Verification: `node --test sitio/pruebas/test_a11y.js` (con jsdom movido) → exit 1 en CI, exit 0 local solo si skip legítimo
  - Roles: role-front, role-back (CI behavior)
  - Test surfaces: `test_a11y.js` (node:test)
  - Files: `sitio/pruebas/test_a11y.js`
  - Scope: Small

- [ ] **Task A4:** `smoke_sh.sh` — Añadir ejecución real de `validate_cycle.py` sobre fixtures cuando `linkml` disponible
  - Acceptance: smoke ejecuta ciclo completo (L1–L4) y falla si `Verdict: FAIL`; CI lo exige
  - Verification: `bash herramientas/linkml/scripts/tests/smoke_sh.sh` en venv con linkml → PASS real
  - Roles: role-back, role-linux
  - Test surfaces: `smoke_sh.sh`, CI job "Validate LinkML Tools"
  - Files: `herramientas/linkml/scripts/tests/smoke_sh.sh`, `.github/workflows/ci.yml`
  - Scope: Small

- [ ] **Task A5:** `check_links.py` — Error exit 2 si arg no existe; rechazar destinos fuera de repo
  - Acceptance: `python3 scripts/check_links.py docs/no-existe.md` → exit 2; `[x](../../../../etc/hostname)` → fail
  - Verification: casos de prueba negativos + `make validate-links` verde en repo limpio
  - Roles: role-back, role-clean-code
  - Test surfaces: `check_links.py` (script CLI)
  - Files: `scripts/check_links.py`
  - Scope: Small

- [ ] **Task A6:** `check-structure.sh` — Exigir ≥1 fichero real en `docs/*` O relajar gate + coherencia `docs/README.md`
  - Acceptance: Decisión binaria implementada; `make validate-structure` verde; `docs/README.md` refleja realidad
  - Verification: `bash scripts/check-structure.sh . --profile P1` → OK; revisar `docs/README.md`
  - Roles: role-linux, role-clean-code
  - Test surfaces: `check-structure.sh`, `validate-structure` make target
  - Files: `scripts/check-structure.sh`, `docs/README.md` (y/o `docs/*/`)
  - Scope: Medium (decisión + implementación)

**Checkpoint: gates-truth**

- [ ] `npm test` pasa (T01–T09 + 9 tests Node)
- [ ] `make validate-links` pasa
- [ ] `make validate-structure` pasa
- [ ] Test negativo por gate: romper a propósito → falla

---

### Phase 2: linkml-robustness (D-002, D-003, D-004, D-006, D-012)

- [ ] **Task B1:** Crear `scripts/_common.py` con `find_linkml`, `run`, `EXIT_*`, `parse_args` base
  - Acceptance: Constantes y helpers centralizados; importable desde `validate_cycle.py` y `linkml_env.py`
  - Verification: `python3 -c "from scripts._common import EXIT_OK, find_linkml; print('OK')"`
  - Roles: role-back, role-clean-code
  - Test surfaces: módulo común
  - Files: `scripts/_common.py` (NEW), `herramientas/linkml/scripts/validate_cycle.py`, `herramientas/linkml/scripts/linkml_env.py`
  - Scope: Medium

- [ ] **Task B2:** `--venv-dir` inexistente → `EXIT_INPUT` (2), sin fallback silencioso a PATH
  - Acceptance: `validate_cycle.py --venv-dir /tmp/no-existe` → exit 2, mensaje claro; mismo comportamiento en `linkml_env.py`
  - Verification: prueba manual + test pytest
  - Roles: role-back
  - Test surfaces: `validate_cycle.py`, `linkml_env.py` (CLI)
  - Files: `scripts/_common.py`, `validate_cycle.py`, `linkml_env.py`
  - Scope: Small

- [ ] **Task B3:** Capa 1 PyYAML `not_run` → warn (no bloqueante) O exigir PyYAML con mensaje coherente
  - Acceptance: Decisión implementada; veredicto no contradice mensaje de capa
  - Verification: `validate_cycle.py` sin PyYAML → warn en L1, PASS/FAIL según capas 2-4
  - Roles: role-back
  - Test surfaces: `validate_cycle.py::layer1_yaml_syntax`
  - Files: `validate_cycle.py`
  - Scope: Small

- [ ] **Task B4:** `bootstrap_arch.sh` — `--dry-run` gana siempre; eliminar `APPLY`; verify usa `$VENV_DIR/bin/python`
  - Acceptance: `--dry-run --apply` → dry-run; `--apply --dry-run` → dry-run; `APPLY` inexistente; verify usa venv python
  - Verification: pruebas de flags ordenadas; `--verify` en Arch usa venv
  - Roles: role-linux, role-back
  - Test surfaces: `bootstrap_arch.sh` (CLI)
  - Files: `herramientas/linkml/scripts/bootstrap_arch.sh`
  - Scope: Small

- [ ] **Task B5:** `os.access(X_OK)` → `EXIT_PERM` (4); `subprocess.run` en `try/except OSError`
  - Acceptance: binario 0644 → exit 4, sin traceback; exit codes canónicos funcionan
  - Verification: `chmod 644 /tmp/fake-linkml; validate_cycle.py --linkml /tmp/fake-linkml` → exit 4
  - Roles: role-back
  - Test surfaces: `find_linkml` (common), `validate_cycle.py`, `linkml_env.py`
  - Files: `scripts/_common.py`, `validate_cycle.py`, `linkml_env.py`
  - Scope: Small

- [ ] **Task B6:** Tests pytest para 4 caminos de fallo (venv inexistente, PyYAML ausente, binario no ejecutable, flags contradictorios)
  - Acceptance: `pytest herramientas/linkml/scripts/tests/` → 4+ tests pass; cubren rutas de error
  - Verification: `pytest herramientas/linkml/scripts/tests/ -v`
  - Roles: role-back, role-linux
  - Test surfaces: `validate_cycle.py`, `linkml_env.py`, `bootstrap_arch.sh`
  - Files: `herramientas/linkml/scripts/tests/test_validate_cycle.py` (NEW), `test_linkml_env.py` (NEW), `test_bootstrap.py` (NEW)
  - Scope: Medium

**Checkpoint: linkml-robustness**

- [ ] `make validate-linkml` pasa (smoke + ciclo real)
- [ ] `pytest herramientas/linkml/scripts/tests/` pasa
- [ ] 4 pruebas manuales de fallo: exit 2, exit 4, warn capa 1, dry-run gana

---

### Phase 3: supply-chain (D-008, D-009, D-011)

- [ ] **Task C1:** `requirements-linkml.lock` con hashes; `pip install --require-hashes`; `pip` fijado
  - Acceptance: `uv pip compile --generate-hashes herramientas/linkml/assets/requirements-linkml.txt -o herramientas/linkml/assets/requirements-linkml.lock`; bootstrap/CI usan `--require-hashes`
  - Verification: `pip install -r herramientas/linkml/assets/requirements-linkml.lock --require-hashes` en venv limpio → árbol idéntico
  - Roles: role-linux, role-back
  - Test surfaces: bootstrap, CI job LinkML
  - Files: `herramientas/linkml/assets/requirements-linkml.lock` (NEW), `bootstrap_arch.sh`, `.github/workflows/ci.yml`
  - Scope: Medium

- [ ] **Task C2:** 9 `uses:` en `ci.yml` por SHA con comentario `# v7`
  - Acceptance: `actionlint .github/workflows/ci.yml` pasa; cada `uses:` = `owner/repo@sha256:... # v7`
  - Verification: `actionlint` + revisión visual
  - Roles: role-linux
  - Test surfaces: CI workflow
  - Files: `.github/workflows/ci.yml`
  - Scope: Small

- [ ] **Task C3:** Renovate — `matchPackageNames`; reglas comodín **antes** de específicas; `pinGitHubActionDigests: true`
  - Acceptance: `renovate-config-validator` sin WARN; dry-run genera PRs agrupados por gestor (npm, github-actions)
  - Verification: `npx --yes --package renovate -- renovate-config-validator .github/renovate.json`; `renovate --platform=local --dry-run` (si posible)
  - Roles: role-linux
  - Test surfaces: Renovate config
  - Files: `.github/renovate.json`
  - Scope: Small

- [ ] **Task C4:** Añadir `gitleaks` pre-commit + CI
  - Acceptance: `.husky/pre-commit` ejecuta `gitleaks detect --staged`; CI job `gitleaks` en workflow
  - Verification: `gitleaks detect --source .` limpio; commit con secreto falso → bloqueado
  - Roles: role-linux, role-back
  - Test surfaces: pre-commit hook, CI
  - Files: `.husky/pre-commit`, `.github/workflows/ci.yml`, `.gitleaks.toml` (NEW si config custom)
  - Scope: Small

**Checkpoint: supply-chain**

- [ ] `actionlint` limpio
- [ ] `renovate-config-validator` sin WARN
- [ ] `gitleaks detect --source .` limpio
- [ ] Lock con hashes instala árbol reproducible

---

### Phase 4: artifacts-docs (D-010, D-014, D-015, D-016, D-007, D-013)

- [ ] **Task D1:** `.archify/README.md` declara generación canónica; borrar 2 superadas (`...111148`)
  - Acceptance: README indica cuál HTML es vigente; `git ls-files .archify/` sin las 2 antiguas; diff legible
  - Verification: `ls -la .archify/`; revisar README
  - Roles: role-clean-code, role-linux
  - Test surfaces: estructura repo
  - Files: `.archify/README.md` (NEW), borrar `.archify/*/architecture-vista-previa-20261113-111148*`, `.archify/*/tree-componentes-20261113-111148*`
  - Scope: Small

- [ ] **Task D2:** Decisión `docs/*`: rellenar stubs mínimos (1 fichero cada una) O relajar gate + `docs/README.md` coherente
  - Acceptance: Opción elegida implementada y coherente con A6
  - Verification: `make validate-structure` + `make validate-docs` verdes
  - Roles: role-linux, role-clean-code
  - Test surfaces: `check-structure.sh`, `docs/README.md`
  - Files: `docs/architecture/`, `docs/guides/`, `docs/runbooks/`, `docs/README.md`
  - Scope: Small

- [ ] **Task D3:** `tasks/todo.md` y `plan.md` — Rutas `/home/alexendros/...` → `scripts/check-structure.sh`
  - Acceptance: `grep -r "/home/alexendros" tasks/` → 0 resultados; comandos Verify usan script vendorizado
  - Verification: `grep -r "/home/alexendros" tasks/`
  - Roles: role-clean-code
  - Test surfaces: documentación tareas
  - Files: `tasks/todo.md`, `tasks/plan.md`
  - Scope: Small

- [ ] **Task D4:** `SECURITY.md` — Frase que concilia «sin LTS» con SLA respuesta
  - Acceptance: Tabla versiones coherente con política; ej: «No hay versiones con soporte LTS; sin embargo, acusaremos recibo en 48h y evaluaremos en 7 días»
  - Verification: leer `SECURITY.md`
  - Roles: role-back, role-clean-code
  - Test surfaces: documentación
  - Files: `SECURITY.md`
  - Scope: Small

- [ ] **Task D5:** T08 — Operar sobre copia temporal O eliminar por tautológico
  - Acceptance: T08 no muta `sitio/index.html`; O tarea eliminada y test removido
  - Verification: `npm run test:sitio` → T08 no toca original; O T08 inexistente
  - Roles: role-front, role-clean-code
  - Test surfaces: `run_checks.py::check_T08`
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [ ] **Task D6:** `.gitignore` — Excepción fechada → `!sitio/pruebas/evidencia/curada/`
  - Acceptance: `.gitignore` sin fechas; directorio `curada/` versionable
  - Verification: `grep "run-2026" .gitignore` → 0; `mkdir -p sitio/pruebas/evidencia/curada && git check-ignore sitio/pruebas/evidencia/curada/foo.json` → no ignorado
  - Roles: role-linux
  - Test surfaces: git ignore rules
  - Files: `.gitignore`
  - Scope: Small

**Checkpoint: artifacts-docs**

- [ ] `make validate-structure` + `validate-docs` + `validate-links` verdes
- [ ] `.archify/` limpio + README canónico
- [ ] `tasks/` sin rutas absolutas
- [ ] `SECURITY.md` coherente

---

### Phase 5: hygiene (D-020, D-021)

- [ ] **Task E1:** Renovate — Migrar `matchPackagePatterns` → `matchPackageNames` (ya en C3, confirmar)
  - Acceptance: `renovate-config-validator` sin WARN de migración
  - Verification: validador
  - Roles: role-linux
  - Files: `.github/renovate.json`
  - Scope: XS

- [ ] **Task E2:** `CODEOWNERS` — Salto de línea final
  - Acceptance: `tail -c1 .github/CODEOWNERS | od -c` → newline
  - Verification: `tail -c1 .github/CODEOWNERS | xxd`
  - Roles: role-clean-code
  - Files: `.github/CODEOWNERS`
  - Scope: XS

- [ ] **Task E3:** Unificar `.nvmrc` y `.node-version`; añadir `.npmrc` con `engine-strict=true`
  - Acceptance: Un solo pin Node; `.npmrc` existe con `engine-strict=true`; `npm ci` en Node 22 falla
  - Verification: `cat .nvmrc .node-version`; `cat .npmrc`; test en Node 22 (opcional)
  - Roles: role-linux
  - Files: `.nvmrc` (o `.node-version`), `.npmrc` (NEW)
  - Scope: XS

- [ ] **Task E4:** `pyproject.toml` con config ruff (line-length=100, target-version=py311); añadir ruff a `make lint`/`lint-fix` y CI
  - Acceptance: `ruff check .` limpio; `make lint` ejecuta ruff; CI job lint incluye ruff
  - Verification: `ruff check .`; `make lint`; CI pass
  - Roles: role-linux, role-back
  - Files: `pyproject.toml` (NEW), `Makefile`, `.github/workflows/ci.yml`
  - Scope: Small

- [ ] **Task E5:** `run_checks.py` — `datetime.UTC` (UP017); un solo `now()` por run_id/generated_at; eliminar `for dep in grep`
  - Acceptance: `ruff check --select UP017` limpio; 1 `now()` en run_checks; `grep` sin bucle
  - Verification: `ruff check sitio/pruebas/run_checks.py scripts/check-structure.sh`
  - Roles: role-clean-code, role-back
  - Files: `sitio/pruebas/run_checks.py`, `scripts/check-structure.sh`
  - Scope: XS

- [ ] **Task E6:** `check_links.py` — `LINK_RE` cubre `[id]: url`; `FENCE_RE` cubre `~~~`; tests
  - Acceptance: Referencias estilo `[id]: url` y cercas `~~~` detectadas; tests unitarios
  - Verification: casos de prueba + `make validate-links`
  - Roles: role-back, role-clean-code
  - Files: `scripts/check_links.py`
  - Scope: Small

**Checkpoint: hygiene**

- [ ] `make lint` limpio (prettier + ruff + shellcheck)
- [ ] `renovate-config-validator` sin WARN
- [ ] `ruff check .` limpio
- [ ] `npm ci` respeta engine-strict

---

## Final Checkpoint: Complete

- [ ] **CP6:** `make validate` → todos sub-gates verdes
- [ ] **CP7:** `npm test` → T01–T09 + 9 tests Node pass
- [ ] **CP8:** CI 5/5 jobs verdes (incluyendo nuevo gitleaks y LinkML real)
- [ ] **CP9:** Test negativo por gate crítico (A1–A6) confirmado

## Risks and Mitigations

| Risk                                    | Impact | Mitigation                                              |
| --------------------------------------- | ------ | ------------------------------------------------------- |
| Decisión `docs/*` bloquea A6/D2         | Medium | Decidir en spec review; stubs mínimos son bajo esfuerzo |
| T08 tautológico: eliminar vs reescribir | Low    | Eliminar (menos riesgo); documentar por qué             |
| PyYAML en capa 1: warn vs exigir        | Medium | Decidir en spec; warn es menos breaking                 |
| `.archify` solo candidate.json          | Medium | Decidir en spec; migración gradual                      |
| Node 22 `engine-strict` rompe CI actual | Low    | CI usa Node 24; `.nvmrc`/.node-version unificado a 24   |

## Open Questions

1. **`docs/*` vacías:** ¿Stubs mínimos o relajar gate? (afecta A6, D2)
2. **`.archify` versionado:** ¿Solo `candidate.json` + build CI? (afecta D1)
3. **PyYAML capa 1:** ¿Warn o exigir? (afecta B3)
4. **T08:** ¿Eliminar o reescribir? (afecta D5)
5. **SECURITY.md:** ¿Qué versiones declarar como "soportadas"? (afecta D4)
