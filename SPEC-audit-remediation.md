# Spec: Auditoría Crítica — Remediación omnigramatekh

> **Fuente:** Auditoría crítica ejecutada en commit `4e3fb83` (2026-11-18).
> 21 defectos (19 confirmados, 2 sospechas) agrupados en 4 bloques + lote higiene.

---

## Capability Map (Phase 0)

| Module id         | Responsibility                                                                                                            | Depends on |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------- |
| gates-truth       | Gates que mienten o se apagan: T01/T06, a11y skip, smoke LinkML, check-links, check-structure                             | —          |
| linkml-robustness | Robustez tooling LinkML: venv fallback, PyYAML, flags, exit codes, código duplicado                                       | —          |
| supply-chain      | Cadena de suministro: lock con hashes, actions por SHA, renovate groups                                                   | —          |
| artifacts-docs    | Artefactos .archify, docs vacías, rutas absolutas, SECURITY.md, test tautológico, .gitignore                              | —          |
| hygiene           | Lote microscópico: renovate migración, CODEOWNERS newline, node pins, engine-strict, ruff, datetime, grep loop, link refs | —          |

**Build order:** `gates-truth` → `linkml-robustness` → `supply-chain` → `artifacts-docs` → `hygiene`
(Independientes entre sí; el orden refleja riesgo/impacto, no dependencia técnica)

---

## Phase 1: Specify

### Objective

Remediar los 21 defectos de la auditoría crítica para que:

- Los gates fallen cuando no verifican y verifiquen contenido cuando dicen verificar
- El tooling LinkML tenga contrato de errores honesto y módulo común sin duplicación
- La cadena de suministro use locks con hashes y actions por SHA
- Los artefactos y documentación sean canónicos, no ruido
- La higiene del repo sea consistente con sus propias reglas

### Tech Stack

- **Proyecto:** Híbrido HTML/Node/Python/Bash/LinkML
- **Node:** 24.x (pnpm/npm, Prettier, Husky, lint-staged, jsdom, axe-core, node:test)
- **Python:** 3.x (LinkML 1.12.1, PyYAML, ruff, bandit)
- **Shell:** POSIX sh (scripts/, .husky/)
- **CI/CD:** GitHub Actions, Renovate
- **Lint/Format:** Prettier (JS/MD/YAML), ruff (Python), shellcheck (Bash)

### Commands

```bash
# Validación completa (gate principal)
make validate

# Validaciones por componente
make validate-structure   # scripts/check-structure.sh --profile P1
make validate-linkml      # smoke Sh + validate_cycle.py real
make validate-docs        # enlaces + estructura docs/
make validate-links       # scripts/check_links.py
make lint                 # prettier --check + ruff check + shellcheck
make lint-fix             # prettier --write + ruff format + shellcheck -f

# Tests
npm test                  # T01–T09 + 9 tests Node (a11y + menu)
npm run test:sitio        # T01–T09 (run_checks.py)
npm run test:js           # 8 tests comportamiento menu.js
node --test sitio/pruebas/test_a11y.js
node --test sitio/pruebas/test_menu.js

# LinkML cycle (manual en venv)
cd herramientas/linkml && python3 scripts/validate_cycle.py \
  --linkml /ruta/a/linkml \
  --schema assets/schema-template.yaml --target-class Catalog \
  --data assets/instance-valid.yaml assets/instance-invalid.yaml

# Renovate
npx --yes --package renovate -- renovate-config-validator .github/renovate.json

# Seguridad
pip install gitleaks  # pre-commit/CI
gitleaks detect --source .
```

### Project Structure (Target Changes)

```
omnigramatekh/
├── scripts/
│   ├── check-structure.sh          # MOD: gates de contenido, no presencia
│   ├── check_links.py              # MOD: error en arg inexistente, confinar repo
│   ├── _common.py                  # NEW: módulo común (find_linkml, run, EXIT_*)
├── sitio/pruebas/
│   ├── run_checks.py               # MOD: T01/T06 detectores forma, T02 parser HTML, T08 copia temporal
│   ├── test_a11y.js                # MOD: catch solo MODULE_NOT_FOUND, CI fail en skip
│   └── test_menu.js                # (sin cambios)
├── herramientas/linkml/scripts/
│   ├── validate_cycle.py           # MOD: common import, not_run=warn, X_OK check, EXIT_PERM
│   ├── linkml_env.py               # MOD: common import, --venv-dir estricto, X_OK check
│   ├── bootstrap_arch.sh           # MOD: $VENV_DIR/bin/python, --dry-run gana, del APPLY
│   ├── smoke_sh.sh                 # MOD: ejecutar validate_cycle.py real
│   └── tests/                      # NEW: pytest para validate_cycle, linkml_env, bootstrap
├── .github/
│   ├── workflows/ci.yml            # MOD: job LinkML ejecuta ciclo real, actions por SHA
│   └── renovate.json               # MOD: matchPackageNames, orden reglas, pin digests
├── .archify/
│   └── README.md                   # NEW: declarar generación canónica
├── docs/
│   ├── architecture/               # DECISION: contenido o relajar gate
│   ├── guides/
│   ├── runbooks/
│   └── README.md                   # MOD: reflejar decisión
├── tasks/
│   ├── todo.md                     # MOD: rutas absolutas → scripts/check-structure.sh
│   └── plan.md                     # MOD: rutas absolutas → scripts/check-structure.sh
├── SECURITY.md                     # MOD: conciliar "sin soporte" con SLA
├── .gitignore                      # MOD: excepción fechada → directorio evidencia/curada/
├── pyproject.toml                  # NEW: config ruff (line-length, etc.)
├── .npmrc                          # NEW: engine-strict=true
├── .nvmrc / .node-version          # UNIFICAR: uno solo
└── CODEOWNERS                      # FIX: salto de línea final
```

### Code Style

- **Python:** ruff (line-length=100, target-version=py311), `datetime.UTC`, un solo `now()` por operación
- **JavaScript/Node:** Prettier (config existente), node:test nativo
- **Shell:** POSIX sh, `set -euo pipefail`, shellcheck clean
- **YAML/Markdown:** Prettier (config existente)
- **Git:** Conventional Commits, una tarea = un commit atómico

### Testing Strategy

- **Unit:** pytest para `scripts/_common.py`, `validate_cycle.py`, `linkml_env.py`
- **Integration:** `make validate` verde (todos los sub-gates)
- **Negative tests:** Por cada gate, test que rompa algo a propósito y verifique fallo
- **LinkML:** `validate_cycle.py` sobre fixtures reales en CI (no solo `--help`)
- **a11y:** Playwright + `@axe-core/playwright` (MEJORA-01, futuro)
- **Coverage:** 100% caminos de error en tooling LinkML; gates críticos con test negativo

### Boundaries

- **Always:**
  - Ejecutar `make validate` antes de commit/push
  - Un commit por defecto (Conventional Commits)
  - Tests negativos para gates nuevos/modificados
  - Re-evaluar roles `role-*` antes de cada tarea de implementación
- **Ask first:**
  - Cambiar decisión: ¿contenido en `docs/*` o relajar `check-structure.sh`?
  - ¿Versionar solo `candidate.json` y generar HTML en CI/release?
  - ¿Migrar tooling LinkML a contenedor OCI como default?
- **Never:**
  - Desactivar gates (T01, T06, a11y) para "arreglar" falsos positivos
  - Commit secrets, `.env` reales, rutas absolutas del HOME
  - Editar `.husky/`, `.github/` sin pasar validación completa

### Success Criteria

| Defecto | Criterio de Éxito                                                                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-019   | T01/T06 pasan con «secretaría/secreto» en contenido; detectan `AKIA...`, `ghp_...`, `BEGIN PRIVATE KEY`, `api_key=...`                                  |
| D-018   | `test_a11y.js`: jsdom roto → exit 1 en CI; skip solo si `MODULE_NOT_FOUND`                                                                              |
| D-017   | Job CI "Validate LinkML Tools" ejecuta `validate_cycle.py` real sobre fixtures y falla si no pasa                                                       |
| D-005   | `check_links.py` arg inexistente → exit 2; enlace fuera repo → fail                                                                                     |
| D-001   | `check-structure.sh` exige ≥1 fichero real en `docs/*` O deja de exigir directorios vacíos; coherente con `docs/README.md`                              |
| D-002   | `--venv-dir` inexistente → `EXIT_INPUT` (2), sin fallback silencioso                                                                                    |
| D-003   | Capa 1 `not_run` → warn, no bloqueante; O exigir PyYAML con mensaje coherente                                                                           |
| D-004   | `--dry-run` gana siempre; `APPLY` eliminado; verify usa `$VENV_DIR/bin/python`                                                                          |
| D-006   | `os.access(X_OK)` → `EXIT_PERM` (4); `subprocess.run` en `try/except OSError`                                                                           |
| D-012   | `find_linkml`, `run`, `EXIT_*` en `scripts/_common.py`; imports en ambos scripts                                                                        |
| D-008   | `requirements-linkml.lock` con hashes; `pip install --require-hashes`; `pip` fijado                                                                     |
| D-009   | 9 `uses:` por SHA con comentario `# v7`; Renovate `pinGitHubActionDigests`                                                                              |
| D-011   | `matchPackageNames`; reglas comodín **antes** de específicas; dry-run Renovate OK                                                                       |
| D-010   | `.archify/README.md` declara canónica; 2 generaciones superadas borradas                                                                                |
| D-014   | `docs/*` con contenido O gate relajado + `docs/README.md` coherente                                                                                     |
| D-015   | `tasks/todo.md` y `plan.md`: rutas `/home/alexendros/...` → `scripts/check-structure.sh`                                                                |
| D-016   | `SECURITY.md`: frase que concilia «sin LTS» con SLA respuesta                                                                                           |
| D-007   | T08 opera sobre copia temporal; O eliminado por tautológico                                                                                             |
| D-013   | `.gitignore`: excepción fechada → `!sitio/pruebas/evidencia/curada/`                                                                                    |
| D-020   | `pyproject.toml` (ruff, line-length); `.npmrc` (engine-strict); `.nvmrc` único; `CODEOWNERS` newline; `datetime.UTC`; un `now()`; sin `for dep in grep` |
| D-021   | `check_links.py`: `LINK_RE` cubre `[id]: url`; `FENCE_RE` cubre `~~~`; tests                                                                            |

### Open Questions

1. **`docs/*` vacías:** ¿Rellenar con stubs mínimos (1 fichero cada una) o relajar `check-structure.sh` para no exigirlas? La auditoría sugiere decisión binaria.
2. **`.archify` versionado:** ¿Mantener HTML versionado (costoso en diff) o solo `candidate.json` + build en CI/release?
3. **LinkML en contenedor:** ¿Hacer que `make validate-linkml` prefiera `docker.io/linkml/linkml@sha256:...` si hay Docker, y solo use venv como fallback?
4. **T08:** ¿Eliminar (tautológico) o reescribir probando un rollback real si existe mecanismo?
5. **SECURITY.md:** ¿Qué versiones "soportadas" declarar? (hoy `0.x | ❌`)

---

## Phase 2: Plan (Preview)

El plan detallado se generará en `tasks/plan-audit.md` tras aprobación de esta spec. Resumen de componentes mayores:

1. **gates-truth** (5 defectos, ~5 tareas): T01/T06, T02, a11y, smoke, check-links, check-structure
2. **linkml-robustness** (5 defectos, ~6 tareas): _common.py, venv estricto, PyYAML, flags, X_OK, tests pytest
3. **supply-chain** (3 defectos, ~4 tareas): lock hashes, actions SHA, renovate migración
4. **artifacts-docs** (6 defectos, ~7 tareas): archify readme, docs decision, tasks paths, SECURITY, T08, gitignore
5. **hygiene** (2 defectos, ~6 tareas): renovate warn, CODEOWNERS, node pins, npmrc, ruff config, link refs

**Checkpoints propuestos:**

- CP1: gates-truth completo → `make validate` sub-gates verdes
- CP2: linkml-robustness completo → `make validate-linkml` verde + pytest pasa
- CP3: supply-chain completo → `renovate-config-validator` sin warn + actions por SHA
- CP4: artifacts-docs completo → `make validate-docs` `validate-links` `validate-structure` verdes
- CP5: hygiene completo → `make lint` limpio + `ruff check` limpio
- CP6: `make validate` completo (todos los sub-gates) + `npm test` + CI 5/5

---

**Siguiente paso:** Aprobar esta spec → generar `tasks/plan-audit.md` y `tasks/todo-audit.md` → implementar por módulos en orden de dependencia.
