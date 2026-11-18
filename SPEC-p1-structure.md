# Spec: Estructura P1 — omnigramatekh

> **Estado: completado.** Ejecutado y publicado en v0.2.0 (2026-11-18).
> El validador vive ahora en `scripts/check-structure.sh` (vendorizado), no en
> la ruta de un skill fuera del repo. Se conserva como registro de la
> especificación.

## Capability Map (Phase 0)

| Module id      | Responsibility                                                                                                    | Depends on |
| -------------- | ----------------------------------------------------------------------------------------------------------------- | ---------- |
| governance     | Archivos de gobernanza (LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, AGENTS, ARCHITECTURE, Makefile, .env.example) | —          |
| ci-cd          | CI/CD y automatización (workflows, CODEOWNERS, renovate, PR template)                                             | governance |
| issues         | Plantillas de issues (bug, feature)                                                                               | governance |
| docs-structure | Estructura de documentación (docs/, subdirectorios, README)                                                       | governance |
| readme-fix     | Meta-sección "Propósito de este documento" en README.md                                                           | —          |

Build order: governance → ci-cd, issues, docs-structure → readme-fix

---

## Phase 1: Specify

### Objective

Completar la estructura de perfil P1 requerida por el canon de la flota (Soluciones-Alexendros) para que `scripts/check-structure.sh` pase sin errores. El repo es un proyecto experimental de diagnóstico y actualización del español-castellano con sitio estático en `sitio/`, herramientas LinkML en `herramientas/linkml/` y documentación en `documentacion/`.

### Tech Stack

- **Proyecto**: Híbrido HTML/Node/LinkML (sin framework web principal)
- **Gestión de dependencias**: npm (package.json existente)
- **CI/CD objetivo**: GitHub Actions (workflow ci.yml)
- **Licencia**: MIT (estándar en la flota)
- **Lenguaje principal**: HTML (documentación y sitio estático)

### Commands

```bash
# Validar estructura P1
bash scripts/check-structure.sh . --profile P1

# Lint/formato (existente)
npm run lint
npx prettier --check .

# Tests existentes
npm test
```

### Project Structure (Target)

```
omnigramatekh/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── CODEOWNERS
│   ├── renovate.json
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug.yml
│       └── feature.yml
├── docs/
│   ├── architecture/
│   ├── guides/
│   ├── runbooks/
│   └── README.md
├── sitio/                 (existente)
├── herramientas/          (existente)
├── documentacion/         (existente)
├── .archify/              (existente)
├── LICENSE                (nuevo)
├── CHANGELOG.md           (nuevo)
├── SECURITY.md            (nuevo)
├── CONTRIBUTING.md        (nuevo)
├── AGENTS.md              (nuevo)
├── ARCHITECTURE.md        (nuevo)
├── Makefile               (nuevo)
├── .env.example           (nuevo)
├── README.md              (existente - añadir sección)
├── package.json           (existente)
├── package-lock.json      (existente)
├── .gitignore             (existente)
├── .prettierrc            (existente)
├── .lintstagedrc          (existente)
└── .husky/                (existente)
```

### Code Style

- **Markdown**: Prettier (config existente), headings ATX (#), una línea en blanco antes/después de headings
- **YAML**: 2 espacios, sin tabs
- **Makefile**: tabs para recetas, variables en UPPER_SNAKE_CASE
- **Shell**: POSIX sh compatible, set -euo pipefail
- **Licencia**: MIT con copyright "Soluciones-Alexendros"

### Testing Strategy

- **Unit**: N/A (archivos estáticos)
- **Integración**: `scripts/check-structure.sh . --profile P1` debe devolver exit 0
- **Smoke**: Verificar que CI workflow es válido con `actionlint`
- **Cobertura**: 100% de archivos P1 requeridos presentes

### Boundaries

- **Always**:
  - Usar plantillas del canon de la flota cuando existan
  - Mantener compatibilidad con estructura existente (sitio/, herramientas/, documentacion/)
  - Validar con `scripts/check-structure.sh` tras cada módulo
- **Ask first**:
  - Cambiar licencia a algo distinto de MIT
  - Añadir dependencias npm nuevas
  - Modificar workflows de CI existentes (no hay)
- **Never**:
  - Borrar o mover directorios existentes
  - Commit secrets o .env reales
  - Editar archivos fuera del scope P1

### Success Criteria

1. `bash scripts/check-structure.sh . --profile P1` → exit 0, sin errores P1
2. Todos los 17 archivos/directorios faltantes creados
3. README.md incluye `### Propósito de este documento`
4. `actionlint` valida `.github/workflows/ci.yml` sin errores
5. `npx prettier --check .` pasa en archivos nuevos/modificados

### Open Questions

1. ¿Contenido específico para AGENTS.md? (¿Usar el AGENTS.md del operador como base?)
2. ¿ARCHITECTURE.md describe la arquitectura actual (sitio estático + LinkML) o una objetivo?
3. ¿Makefile targets estándar: `test`, `lint`, `validate`, `clean`?
4. ¿CODEOWNERS: @Soluciones-Alexendros/owners o @alexendros?
