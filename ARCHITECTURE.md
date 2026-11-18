# Arquitectura — omnigramatekh

### Propósito de este documento

Describe la arquitectura **actual** del repositorio (v0.1.0, experimental): cuatro pilares aislados (sitio estático, herramientas LinkML, documentación, diagramas Archify), dependencias externas, flujos de datos, ADRs, y extensibilidad futura no comprometida.

---

> **Estado**: Actual (v0.1.0, experimental) — _No describe un estado objetivo futuro._

## Visión General

**OmniGramatekh** es un repositorio de trabajo experimental para diagnóstico y actualización del español-castellano. No es un producto desplegado ni un servicio en producción. Consta de cuatro pilares independientes que conviven en el mismo repo:

```
┌─────────────────────────────────────────────────────────────┐
│                      omnigramatekh                          │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│   sitio/    │ herramientas│ documentacion│     .archify/    │
│  (estático) │  (LinkML)   │  (ADRs,specs)│   (diagramas)    │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

Cada pilar es **aislado**: no hay acoplamiento en tiempo de ejecución, ni dependencias compartidas, ni build pipeline unificado.

---

## 1. Sitio Estático (`sitio/`)

**Propósito**: Portada experimental y prueba de concepto. No publicado.

- **Tecnología**: HTML5 + CSS3 + JS vanilla (sin framework)
- **Servidor local**: `python3 -m http.server 8765 --bind 127.0.0.1`
- **Estructura**:
  ```
  sitio/
  ├── index.html          # Página principal
  ├── css/                # Estilos
  ├── js/                 # Scripts mínimos
  ├── pruebas/            # Scripts de validación local
  └── assets/             # Recursos estáticos
  ```
- **Validación**: `npm test` ejecuta `python3 sitio/pruebas/run_checks.py`
- **Despliegue**: Ninguno (archivos servidos directamente)

---

## 2. Herramientas LinkML (`herramientas/linkml/`)

**Propósito**: Modelado léxico con LinkML, validadores, bootstrap de entorno.

- **Tecnología**: Python (LinkML), Node.js (scripts auxiliares), YAML/JSON
- **Componentes clave**:
  - `scripts/linkml_env.py` — Verifica entorno LinkML
  - `scripts/tests/smoke_sh.sh` — Smoke test read-only
  - `SPEC-modelo-linkml.md` — Especificación del modelo (en `documentacion/linkml/`)
  - ADR 0002 — Decisión de incorporación
- **Entrada**: Esquemas YAML LinkML (por definir)
- **Salida**: Clases Python, JSON Schema, documentación generada
- **Validación**: `bash herramientas/linkml/scripts/tests/smoke_sh.sh`

---

## 3. Documentación (`documentacion/`)

**Propósito**: Conocimiento técnico, decisiones, especificaciones.

- **Estructura**:
  ```
  documentacion/
  ├── adr/                    # Architecture Decision Records
  │   ├── 0001-sitio-estatico-aislado.md
  │   └── 0002-incorporacion-herramientas-linkml.md
  ├── linkml/
  │   └── SPEC-modelo-linkml.md
  └── SPEC-p1-structure.md    # Este repo: spec estructura P1
  ```
- **Formato**: Markdown + frontmatter YAML opcional
- **Validación**: `npx prettier --check documentacion/`

---

## 4. Diagramas Archify (`.archify/`)

**Propósito**: Diagramas HTML autónomos, explorables, con exportación.

- **Tecnología**: Archify (Mermaid → HTML standalone)
- **Tipos**: Arquitectura, flujo, árbol, entidades, timeline, waterfall
- **Temas**: Dark/Light, motion, export SVG/WebM/PNG
- **Uso**: Documentación viva, onboarding, comunicación técnica

---

## Dependencias Externas

| Dependencia    | Uso                                        | Gestión                              |
| -------------- | ------------------------------------------ | ------------------------------------ |
| Node.js / npm  | Tooling (prettier, lint, test runner)      | `package.json` + `package-lock.json` |
| Python 3.11+   | LinkML, scripts validación, servidor local | Sistema / `venv` opcional            |
| GitHub Actions | CI/CD                                      | `.github/workflows/ci.yml`           |
| Renovate       | Actualización dependencias                 | `.github/renovate.json`              |

**No hay**: Base de datos, message queue, cache, search, object storage, auth service, API gateway.

---

## Flujos de Datos (Resumen)

```
Usuario → Navegador → sitio/index.html (estático)
           ↓
    Validación local (npm test) → run_checks.py → OK/FAIL

Desarrollador → LinkML schemas → herramientas/linkml/ → Python classes / JSON Schema
           ↓
    Validación (smoke_sh.sh) → OK/FAIL

Documentación → Markdown → documentacion/ / docs/ → Lectura humana
           ↓
    Diagramas → .archify/ → HTML standalone → Navegador
```

---

## Decisiones Arquitectónicas Clave (ADRs)

| ADR  | Título                            | Estado   | Impacto                                 |
| ---- | --------------------------------- | -------- | --------------------------------------- |
| 0001 | Sitio estático aislado            | Aceptado | Sin build, sin deploy, sin acoplamiento |
| 0002 | Incorporación herramientas LinkML | Aceptado | LinkML como librería, no framework      |

Ver `documentacion/adr/` para detalle.

---

## Métricas y Observabilidad

- **No hay**: Logs centralizados, métricas, tracing, alerting, dashboards.
- **Validación**: Solo CI (lint, test, estructura) y scripts locales.

---

## Seguridad

- **Superficie de ataque**: Mínima (archivos estáticos, sin backend).
- **Dependencias**: Solo `devDependencies` en `package.json` (prettier, lint-staged, husky).
- **Política**: Ver `SECURITY.md`.

---

## Extensibilidad Futura (No Comprometido)

Si el proyecto evoluciona, áreas candidatas:

- **Modelo LinkML completo** → Generación de código, API de validación
- **Sitio publicado** → Astro/Next.js + despliegue estático (Vercel/Netlify/GitHub Pages)
- **Pipeline unificado** → Makefile targets coordinados, CI matrix

> **Nota**: Cualquier cambio arquitectónico requerirá ADR nuevo y actualización de este documento.
