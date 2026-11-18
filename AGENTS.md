# Contexto del Agente — omnigramatekh

### Propósito de este documento

Define el contexto operativo para agentes de IA (y humanos) que trabajen en este repositorio: principios, estructura, comandos de verificación, reglas de Git/seguridad, skills disponibles y referencias rápidas.

---

Este archivo guía a agentes de IA (y humanos) que trabajen en este repositorio.

## Principios

- **Idioma**: Español, conciso, sin emojis ni relleno.
- **Verificación**: Nada se da por terminado sin validar con el comando del repo.
- **Autonomía**: Modo «palante» por defecto para pasos rutinarios (leer, editar, crear, testear, commit).
- **Confirmación**: Solo para pasos irreversibles o de radio amplio (force-push, borrado de datos, credenciales).

## Dónde vive el código

```
omnigramatekh/
├── sitio/                 # Sitio estático (portada experimental)
├── herramientas/          # Herramientas LinkML (modelado, validadores, env)
├── documentacion/         # Documentación técnica, ADRs, specs
├── .archify/              # Diagramas HTML autónomos (archify)
├── docs/                  # Docs de usuario (architecture, guides, runbooks)
├── .github/               # CI/CD, templates, renovate
├── tasks/                 # Planes y tareas (project-status, plan-specification)
└── SPEC-*.md              # Especificaciones de features
```

## Verificación por componente

| Componente          | Stack          | Comando de validación                                |
| ------------------- | -------------- | ---------------------------------------------------- |
| Sitio estático      | HTML/CSS/JS    | `cd sitio && python3 -m http.server 8765` (manual)   |
| Sitio: checks       | Python + Node  | `npm test` (T01–T09 + 8 pruebas de `menu.js`)        |
| Herramientas LinkML | Python/Node    | `bash herramientas/linkml/scripts/tests/smoke_sh.sh` |
| Documentación       | Markdown       | `make validate-docs`                                 |
| Estructura P1       | Canon flota    | `bash scripts/check-structure.sh . --profile P1`     |
| CI/CD               | GitHub Actions | `actionlint .github/workflows/ci.yml`                |
| General             | Node           | `npm test` / `make validate`                         |

## Reglas de Git

- Commit y push a ramas de trabajo sin pedir permiso.
- `--force` y reescritura de historia: **sí se pide confirmación**.
- Mensajes: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, etc.)
- Branches: `feat/`, `fix/`, `docs/`, `chore/`, `ci/`

## Reglas de Seguridad

- **Secretos**: Nunca en el repo ni en `.pi/mcp.json` de proyecto. Usar variables de entorno o `!comando`.
- **Gate de seguridad**: `~/.pi/agent/extensions/path-guard.ts` bloquea escritura fuera de `~/Work/` y en rutas de credenciales (`.ssh`, `.gnupg`, `.aws`, `.kube`, `auth.json`, `mcp-auth.json`).
- **No tocar**: `~/.config/hypr/`, `~/.pi/agent/settings.json`, `mcp.json`, `auth.json`, `extensions/`, `skills/` sin permiso.

## Skills Disponibles (machineroom)

Los skills se cargan desde `~/.pi/agent/skills/`. Principales:

- `project-status` — observar, higienizar, cerrar increments
- `plan-specification` — especificar, planificar, taskear, implementar
- `role-linux` — packaging, CI/CD, dependencias, compatibilidad
- `role-back` — backend, APIs, persistencia, jobs
- `role-front` — frontend, estado cliente, routing
- `role-clean-code` — refactoring, clean code
- `web-owasp` / `web-compliance` / `web-performance` — auditorías web
- `archify` — diagramas HTML explorables
- `omarchy` / `omarchy-app` — desktop Linux (solo si se toca `~/.config/`)

## Antes de Afirmar

- APIs, versiones, flags: consultar vía `context7` (codemode).
- PRs, issues, logs Actions: MCP `github`.
- Navegador/medición web: `playwright` o `chrome-devtools` (codemode).

## Comandos Útiles

```bash
# Gate completo (lint + tests + estructura P1 + smoke LinkML)
make validate

# Validar estructura P1 (script vendorizado: sin rutas del HOME)
bash scripts/check-structure.sh . --profile P1

# Tests del sitio y del menú
npm test              # ambas suites
npm run test:sitio    # T01–T09
npm run test:js       # 8 pruebas de comportamiento de menu.js

# Formato
make lint             # comprueba
make lint-fix         # reescribe

# Smoke LinkML
bash herramientas/linkml/scripts/tests/smoke_sh.sh
```

## Política de artefactos

- `.archify/`: se versionan el `.html` y su `candidate.json`. Los recibos
  (`*.delivery.json`, `*.finalize*.json`, `*.browser-check.json`) y los
  directorios `review-*/` son regenerables, contienen rutas absolutas y no se
  versionan.
- `sitio/pruebas/evidencia/`: solo se versionan las corridas curadas
  (`run-20261113T*.json`); `latest.json` y las corridas nuevas son estado local.
- `docs/` es documentación de uso; `documentacion/` es el canon técnico (ADRs y
  especificaciones). Si discrepan, manda `documentacion/`.
