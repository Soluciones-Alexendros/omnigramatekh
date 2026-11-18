# Guía de Contribución

### Propósito de este documento

Guía completa para contribuir al repositorio: código de conducta, flujo de trabajo (fork, rama, PR), convenciones de commits y código, validaciones locales, reporte de issues, y estructura del proyecto.

---

Gracias por tu interés en contribuir a **OmniGramatekh**.

## Código de Conducta

Este proyecto sigue el [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Al participar, se espera que mantengas este código. Reporta conductas inaceptables a conduct@alexendros.dev.

## Cómo Contribuir

### 1. Preparar el entorno

```bash
# Clonar el repo
git clone https://github.com/Soluciones-Alexendros/omnigramatekh.git
cd omnigramatekh

# Instalar dependencias
npm ci

# Verificar que todo funciona
make validate
```

### 2. Flujo de trabajo

1. **Fork** el repositorio
2. Crea una rama: `git checkout -b feat/mi-mejora` (o `fix/`, `docs/`, `chore/`)
3. Haz tus cambios siguiendo las convenciones
4. Ejecuta validaciones: `make validate`
5. Commit con mensaje convencional: `git commit -m "feat: añadir nueva característica"`
6. Push y abre un **Pull Request**

### 3. Convenciones

#### Commits (Conventional Commits)

```
<type>[scope]: <description>

[body]

[footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`

**Ejemplos**:

- `feat(linkml): añadir validador de esquemas`
- `fix(sitio): corregir ruta rota en navegación`
- `docs: actualizar README con nuevo propósito`

#### Código

- **Markdown**: Prettier (`.prettierrc`), headings ATX (`#`), una línea en blanco antes/después
- **YAML**: 2 espacios, sin tabs
- **Shell**: POSIX `sh` compatible, `set -euo pipefail`
- **Python**: `ruff` + `black` (si se añaden scripts)
- **JavaScript/TypeScript**: ESLint + Prettier (config existente)

#### Pull Requests

- Usa la plantilla (`.github/PULL_REQUEST_TEMPLATE.md`)
- Un PR = un cambio lógico
- Incluye tests si añades funcionalidad
- Actualiza docs si cambias comportamiento
- CI debe pasar (lint, test, validate)

### 4. Validaciones Locales

```bash
# Todo (lint + test + validate estructura)
make validate

# Solo lint
make lint

# Solo tests
make test

# Validar estructura P1
make validate-structure
```

### 5. Reportar Issues

- **Bugs**: usa la plantilla `.github/ISSUE_TEMPLATE/bug.yml`
- **Features**: usa la plantilla `.github/ISSUE_TEMPLATE/feature.yml`
- **Seguridad**: ver `SECURITY.md` (no issues públicos)

## Estructura del Proyecto

```
omnigramatekh/
├── sitio/                 # Sitio estático (HTML/CSS/JS)
├── herramientas/          # Herramientas LinkML y scripts
├── documentacion/         # Documentación técnica y ADRs
├── .archify/              # Diagramas HTML autónomos
├── docs/                  # Docs de usuario (architecture, guides, runbooks)
└── .github/               # CI/CD, templates, renovate
```

## Preguntas

Abre un issue con label `question` o contacta a maintainers.
