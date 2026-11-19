# Tasks: Auditoría Crítica — Remediación omnigramatekh

> **Estado: completado y publicado en v0.3.0** (2026-11-19).
> PRs #5 (remediación), #6 (MEJORA-01), #7 (MEJORA-03), #8 (MEJORA-05),
> #9 (MEJORA-04), #10 (MEJORA-02) y #11 (release). CI 12/12 y CodeQL en verde.
> Excepción documentada: mutación (mutmut) descartada con motivo en
> `SPEC-mejora-02-validator-suite.md`; no se declara métrica no medida.
>
> Generado desde `SPEC-audit-remediation.md` y `plan-audit.md`.
> Una tarea = un commit atómico (Conventional Commits).
> Antes de cada tarea: re-evaluar roles `role-*` e invocar los que apliquen.

---

## Module: gates-truth (D-019, D-018, D-017, D-005, D-001)

- [x] **Task A1:** T01/T06 — Detectores de forma (regex claves reales) + caso prueba «secretaría»
  - Acceptance: T01/T06 pasan con «La secretaría guarda el secreto»; detectan `AKIA[0-9A-Z]{16}`, `ghp_[a-zA-Z0-9]{36}`, `-----BEGIN.*PRIVATE KEY-----`, `(?i)(api[_-]?key|password|token)\s*[:=]\s*['"]\S{8,}`
  - Implementation roles: role-front, role-clean-code
  - Test surfaces: `run_checks.py::check_T01`, `run_checks.py::check_T06`
  - Verify: `npm run test:sitio` (T01–T09 pass) + test negativo añadiendo secreto real → fail
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [x] **Task A2:** T02 — Parsear HTML con `html.parser` / selector por `id`, no `split`
  - Acceptance: T02 pasa independientemente del orden de secciones; test con secciones reordenadas
  - Implementation roles: role-front, role-clean-code
  - Test surfaces: `run_checks.py::check_T02`
  - Verify: `npm run test:sitio` + test manual reordenando secciones en copia
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [x] **Task A3:** `test_a11y.js` — Catch solo `MODULE_NOT_FOUND`; en CI (`process.env.CI`) convertir skip en fallo
  - Acceptance: jsdom roto → exit 1 en CI; skip solo si módulo no instalado; comentario actualizado
  - Implementation roles: role-front, role-back
  - Test surfaces: `test_a11y.js` (node:test)
  - Verify: `node --test sitio/pruebas/test_a11y.js` (con jsdom movido) → exit 1 en CI, exit 0 local solo si skip legítimo
  - Files: `sitio/pruebas/test_a11y.js`
  - Scope: Small

- [x] **Task A4:** `smoke_sh.sh` — Ejecutar `validate_cycle.py` real sobre fixtures cuando `linkml` disponible
  - Acceptance: smoke ejecuta ciclo completo (L1–L4) y falla si `Verdict: FAIL`; CI lo exige
  - Implementation roles: role-back, role-linux
  - Test surfaces: `smoke_sh.sh`, CI job "Validate LinkML Tools"
  - Verify: `bash herramientas/linkml/scripts/tests/smoke_sh.sh` en venv con linkml → PASS real
  - Files: `herramientas/linkml/scripts/tests/smoke_sh.sh`, `.github/workflows/ci.yml`
  - Scope: Small

- [x] **Task A5:** `check_links.py` — Error exit 2 si arg no existe; rechazar destinos fuera de repo
  - Acceptance: `python3 scripts/check_links.py docs/no-existe.md` → exit 2; `[x](../../../../etc/hostname)` → fail
  - Implementation roles: role-back, role-clean-code
  - Test surfaces: `check_links.py` (script CLI)
  - Verify: casos de prueba negativos + `make validate-links` verde en repo limpio
  - Files: `scripts/check_links.py`
  - Scope: Small

- [x] **Task A6:** `check-structure.sh` — Exigir ≥1 fichero real en `docs/*` O relajar gate + coherencia `docs/README.md`
  - Acceptance: Decisión binaria implementada; `make validate-structure` verde; `docs/README.md` refleja realidad
  - Implementation roles: role-linux, role-clean-code
  - Test surfaces: `check-structure.sh`, `validate-structure` make target
  - Verify: `bash scripts/check-structure.sh . --profile P1` → OK; revisar `docs/README.md`
  - Files: `scripts/check-structure.sh`, `docs/README.md` (y/o `docs/*/`)
  - Scope: Medium

## Checkpoint: gates-truth

- [x] `npm test` pasa (T01–T09 + 9 tests Node)
- [x] `make validate-links` pasa
- [x] `make validate-structure` pasa
- [x] Test negativo por gate: romper a propósito → falla

---

## Module: linkml-robustness (D-002, D-003, D-004, D-006, D-012)

- [x] **Task B1:** Crear `scripts/_common.py` con `find_linkml`, `run`, `EXIT_*`, `parse_args` base
  - Acceptance: Constantes y helpers centralizados; importable desde `validate_cycle.py` y `linkml_env.py`
  - Implementation roles: role-back, role-clean-code
  - Test surfaces: módulo común
  - Verify: `python3 -c "from scripts._common import EXIT_OK, find_linkml; print('OK')"`
  - Files: `scripts/_common.py` (NEW), `herramientas/linkml/scripts/validate_cycle.py`, `herramientas/linkml/scripts/linkml_env.py`
  - Scope: Medium

- [x] **Task B2:** `--venv-dir` inexistente → `EXIT_INPUT` (2), sin fallback silencioso a PATH
  - Acceptance: `validate_cycle.py --venv-dir /tmp/no-existe` → exit 2, mensaje claro; mismo comportamiento en `linkml_env.py`
  - Implementation roles: role-back
  - Test surfaces: `validate_cycle.py`, `linkml_env.py` (CLI)
  - Verify: prueba manual + test pytest
  - Files: `scripts/_common.py`, `validate_cycle.py`, `linkml_env.py`
  - Scope: Small

- [x] **Task B3:** Capa 1 PyYAML `not_run` → warn (no bloqueante) O exigir PyYAML con mensaje coherente
  - Acceptance: Decisión implementada; veredicto no contradice mensaje de capa
  - Implementation roles: role-back
  - Test surfaces: `validate_cycle.py::layer1_yaml_syntax`
  - Verify: `validate_cycle.py` sin PyYAML → warn en L1, PASS/FAIL según capas 2-4
  - Files: `validate_cycle.py`
  - Scope: Small

- [x] **Task B4:** `bootstrap_arch.sh` — `--dry-run` gana siempre; eliminar `APPLY`; verify usa `$VENV_DIR/bin/python`
  - Acceptance: `--dry-run --apply` → dry-run; `--apply --dry-run` → dry-run; `APPLY` inexistente; verify usa venv python
  - Implementation roles: role-linux, role-back
  - Test surfaces: `bootstrap_arch.sh` (CLI)
  - Verify: pruebas de flags ordenadas; `--verify` en Arch usa venv
  - Files: `herramientas/linkml/scripts/bootstrap_arch.sh`
  - Scope: Small

- [x] **Task B5:** `os.access(X_OK)` → `EXIT_PERM` (4); `subprocess.run` en `try/except OSError`
  - Acceptance: binario 0644 → exit 4, sin traceback; exit codes canónicos funcionan
  - Implementation roles: role-back
  - Test surfaces: `find_linkml` (common), `validate_cycle.py`, `linkml_env.py`
  - Verify: `chmod 644 /tmp/fake-linkml; validate_cycle.py --linkml /tmp/fake-linkml` → exit 4
  - Files: `scripts/_common.py`, `validate_cycle.py`, `linkml_env.py`
  - Scope: Small

- [x] **Task B6:** Tests pytest para 4 caminos de fallo (venv inexistente, PyYAML ausente, binario no ejecutable, flags contradictorios)
  - Acceptance: `pytest herramientas/linkml/scripts/tests/` → 4+ tests pass; cubren rutas de error
  - Implementation roles: role-back, role-linux
  - Test surfaces: `validate_cycle.py`, `linkml_env.py`, `bootstrap_arch.sh`
  - Verify: `pytest herramientas/linkml/scripts/tests/ -v`
  - Files: `herramientas/linkml/scripts/tests/test_validate_cycle.py` (NEW), `test_linkml_env.py` (NEW), `test_bootstrap.py` (NEW)
  - Scope: Medium

## Checkpoint: linkml-robustness

- [x] `make validate-linkml` pasa (smoke + ciclo real)
- [x] `pytest herramientas/linkml/scripts/tests/` pasa
- [x] 4 pruebas manuales de fallo: exit 2, exit 4, warn capa 1, dry-run gana

---

## Module: supply-chain (D-008, D-009, D-011)

- [x] **Task C1:** `requirements-linkml.lock` con hashes; `pip install --require-hashes`; `pip` fijado
  - Acceptance: `uv pip compile --generate-hashes herramientas/linkml/assets/requirements-linkml.txt -o herramientas/linkml/assets/requirements-linkml.lock`; bootstrap/CI usan `--require-hashes`
  - Implementation roles: role-linux, role-back
  - Test surfaces: bootstrap, CI job LinkML
  - Verify: `pip install -r herramientas/linkml/assets/requirements-linkml.lock --require-hashes` en venv limpio → árbol idéntico
  - Files: `herramientas/linkml/assets/requirements-linkml.lock` (NEW), `bootstrap_arch.sh`, `.github/workflows/ci.yml`
  - Scope: Medium

- [x] **Task C2:** 9 `uses:` en `ci.yml` por SHA con comentario `# v7`
  - Acceptance: `actionlint .github/workflows/ci.yml` pasa; cada `uses:` = `owner/repo@sha256:... # v7`
  - Implementation roles: role-linux
  - Test surfaces: CI workflow
  - Verify: `actionlint` + revisión visual
  - Files: `.github/workflows/ci.yml`
  - Scope: Small

- [x] **Task C3:** Renovate — `matchPackageNames`; reglas comodín **antes** de específicas; `pinGitHubActionDigests: true`
  - Acceptance: `renovate-config-validator` sin WARN; dry-run genera PRs agrupados por gestor (npm, github-actions)
  - Implementation roles: role-linux
  - Test surfaces: Renovate config
  - Verify: `npx --yes --package renovate -- renovate-config-validator .github/renovate.json`; `renovate --platform=local --dry-run` (si posible)
  - Files: `.github/renovate.json`
  - Scope: Small

- [x] **Task C4:** Añadir `gitleaks` pre-commit + CI
  - Acceptance: `.husky/pre-commit` ejecuta `gitleaks detect --staged`; CI job `gitleaks` en workflow
  - Implementation roles: role-linux, role-back
  - Test surfaces: pre-commit hook, CI
  - Verify: `gitleaks detect --source .` limpio; commit con secreto falso → bloqueado
  - Files: `.husky/pre-commit`, `.github/workflows/ci.yml`, `.gitleaks.toml` (NEW si config custom)
  - Scope: Small

## Checkpoint: supply-chain

- [x] `actionlint` limpio
- [x] `renovate-config-validator` sin WARN
- [x] `gitleaks detect --source .` limpio
- [x] Lock con hashes instala árbol reproducible

---

## Module: artifacts-docs (D-010, D-014, D-015, D-016, D-007, D-013)

- [x] **Task D1:** `.archify/README.md` declara generación canónica; borrar 2 superadas (`...111148`)
  - Acceptance: README indica cuál HTML es vigente; `git ls-files .archify/` sin las 2 antiguas; diff legible
  - Implementation roles: role-clean-code, role-linux
  - Test surfaces: estructura repo
  - Verify: `ls -la .archify/`; revisar README
  - Files: `.archify/README.md` (NEW), borrar `.archify/*/architecture-vista-previa-20261113-111148*`, `.archify/*/tree-componentes-20261113-111148*`
  - Scope: Small

- [x] **Task D2:** Decisión `docs/*`: rellenar stubs mínimos (1 fichero cada una) O relajar gate + `docs/README.md` coherente
  - Acceptance: Opción elegida implementada y coherente con A6
  - Implementation roles: role-linux, role-clean-code
  - Test surfaces: `check-structure.sh`, `docs/README.md`
  - Verify: `make validate-structure` + `make validate-docs` verdes
  - Files: `docs/architecture/`, `docs/guides/`, `docs/runbooks/`, `docs/README.md`
  - Scope: Small

- [x] **Task D3:** `tasks/todo.md` y `plan.md` — Rutas `/home/alexendros/...` → `scripts/check-structure.sh`
  - Acceptance: `grep -r "/home/alexendros" tasks/` → 0 resultados; comandos Verify usan script vendorizado
  - Implementation roles: role-clean-code
  - Test surfaces: documentación tareas
  - Verify: `grep -r "/home/alexendros" tasks/`
  - Files: `tasks/todo.md`, `tasks/plan.md`
  - Scope: Small

- [x] **Task D4:** `SECURITY.md` — Frase que concilia «sin LTS» con SLA respuesta
  - Acceptance: Tabla versiones coherente con política; ej: «No hay versiones con soporte LTS; sin embargo, acusaremos recibo en 48h y evaluaremos en 7 días»
  - Implementation roles: role-back, role-clean-code
  - Test surfaces: documentación
  - Verify: leer `SECURITY.md`
  - Files: `SECURITY.md`
  - Scope: Small

- [x] **Task D5:** T08 — Operar sobre copia temporal O eliminar por tautológico
  - Acceptance: T08 no muta `sitio/index.html`; O tarea eliminada y test removido
  - Implementation roles: role-front, role-clean-code
  - Test surfaces: `run_checks.py::check_T08`
  - Verify: `npm run test:sitio` → T08 no toca original; O T08 inexistente
  - Files: `sitio/pruebas/run_checks.py`
  - Scope: Small

- [x] **Task D6:** `.gitignore` — Excepción fechada → `!sitio/pruebas/evidencia/curada/`
  - Acceptance: `.gitignore` sin fechas; directorio `curada/` versionable
  - Implementation roles: role-linux
  - Test surfaces: git ignore rules
  - Verify: `grep "run-2026" .gitignore` → 0; `mkdir -p sitio/pruebas/evidencia/curada && git check-ignore sitio/pruebas/evidencia/curada/foo.json` → no ignorado
  - Files: `.gitignore`
  - Scope: Small

## Checkpoint: artifacts-docs

- [x] `make validate-structure` + `validate-docs` + `validate-links` verdes
- [x] `.archify/` limpio + README canónico
- [x] `tasks/` sin rutas absolutas
- [x] `SECURITY.md` coherente

---

## Module: hygiene (D-020, D-021)

- [x] **Task E1:** Renovate — Confirmar `matchPackagePatterns` → `matchPackageNames` (ya en C3)
  - Acceptance: `renovate-config-validator` sin WARN de migración
  - Implementation roles: role-linux
  - Test surfaces: Renovate config
  - Verify: validador
  - Files: `.github/renovate.json`
  - Scope: XS

- [x] **Task E2:** `CODEOWNERS` — Salto de línea final
  - Acceptance: `tail -c1 .github/CODEOWNERS | od -c` → newline
  - Implementation roles: role-clean-code
  - Test surfaces: formato archivo
  - Verify: `tail -c1 .github/CODEOWNERS | xxd`
  - Files: `.github/CODEOWNERS`
  - Scope: XS

- [x] **Task E3:** Unificar `.nvmrc` y `.node-version`; añadir `.npmrc` con `engine-strict=true`
  - Acceptance: Un solo pin Node; `.npmrc` existe con `engine-strict=true`; `npm ci` en Node 22 falla
  - Implementation roles: role-linux
  - Test surfaces: configuración Node
  - Verify: `cat .nvmrc .node-version`; `cat .npmrc`; test en Node 22 (opcional)
  - Files: `.nvmrc` (o `.node-version`), `.npmrc` (NEW)
  - Scope: XS

- [x] **Task E4:** `pyproject.toml` con config ruff (line-length=100, target-version=py311); añadir ruff a `make lint`/`lint-fix` y CI
  - Acceptance: `ruff check .` limpio; `make lint` ejecuta ruff; CI job lint incluye ruff
  - Implementation roles: role-linux, role-back
  - Test surfaces: lint Python
  - Verify: `ruff check .`; `make lint`; CI pass
  - Files: `pyproject.toml` (NEW), `Makefile`, `.github/workflows/ci.yml`
  - Scope: Small

- [x] **Task E5:** `run_checks.py` — `datetime.UTC` (UP017); un solo `now()` por run_id/generated_at; eliminar `for dep in grep`
  - Acceptance: `ruff check --select UP017` limpio; 1 `now()` en run_checks; `grep` sin bucle
  - Implementation roles: role-clean-code, role-back
  - Test surfaces: lint Python
  - Verify: `ruff check sitio/pruebas/run_checks.py scripts/check-structure.sh`
  - Files: `sitio/pruebas/run_checks.py`, `scripts/check-structure.sh`
  - Scope: XS

- [x] **Task E6:** `check_links.py` — `LINK_RE` cubre `[id]: url`; `FENCE_RE` cubre `~~~`; tests
  - Acceptance: Referencias estilo `[id]: url` y cercas `~~~` detectadas; tests unitarios
  - Implementation roles: role-back, role-clean-code
  - Test surfaces: `check_links.py`
  - Verify: casos de prueba + `make validate-links`
  - Files: `scripts/check_links.py`
  - Scope: Small

## Checkpoint: hygiene

- [x] `make lint` limpio (prettier + ruff + shellcheck)
- [x] `renovate-config-validator` sin WARN
- [x] `ruff check .` limpio
- [x] `npm ci` respeta engine-strict

---

## Final Checkpoints

- [x] **CP-Final:** `make validate` → todos sub-gates verdes
- [x] **CP-Final:** `npm test` → T01–T09 + 9 tests Node pass
- [x] **CP-Final:** CI 5/5 jobs verdes (incluyendo nuevo gitleaks y LinkML real)
- [x] **CP-Final:** Test negativo por gate crítico (A1–A6) confirmado

---

## Notes for Implementation

- **Roles:** Antes de CADA tarea, re-evaluar y cargar `role-front`, `role-back`, `role-linux`, `role-clean-code` según `Test surfaces` e `Implementation roles` declarados.
- **Commits:** `feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `refactor:` según tipo. Un commit por tarea.
- **Verificación:** Ejecutar comandos `Verify` de la tarea ANTES de marcar completada.
- **Checkpoints:** No avanzar al siguiente módulo sin pasar el checkpoint del actual.

---

## Resultado verificado (2026-11-19)

| Comprobación                         | Resultado                                                                |
| ------------------------------------ | ------------------------------------------------------------------------ |
| `make validate`                      | PASS (lint + test + contratos + estructura P1 + LinkML + docs + enlaces) |
| `pytest -q`                          | 42 tests                                                                 |
| `npm test`                           | T01–T09 del sitio (T07 sin datos de campo) + 9 tests JS                  |
| `npm run test:browser`               | T04b contraste real + T03b reflow + Lighthouse con presupuestos          |
| CI en `main`                         | CI 12/12, CodeQL, OpenSSF Scorecard en verde                             |
| `gitleaks` / `zizmor` / `actionlint` | Limpios, con versiones fijadas                                           |
