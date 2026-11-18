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

| Componente          | Stack          | Comando de validación                                                                        |
| ------------------- | -------------- | -------------------------------------------------------------------------------------------- |
| Sitio estático      | HTML/CSS/JS    | `cd sitio && python3 -m http.server 8765` (manual)                                           |
| Herramientas LinkML | Python/Node    | `bash herramientas/linkml/scripts/tests/smoke_sh.sh`                                         |
| Documentación       | Markdown       | `npx prettier --check documentacion/`                                                        |
| Estructura P1       | Canon flota    | `bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .` |
| CI/CD               | GitHub Actions | `actionlint .github/workflows/ci.yml`                                                        |
| General             | Node           | `npm test` / `make validate`                                                                 |

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
# Estado del repo (project-status)
python /home/alexendros/.pi/agent/skills/project-status/scripts/inicio_plan.py . --out /tmp/status

# Validar estructura P1
bash /home/alexendros/.pi/agent/skills/project-status/scripts/check-product-structure.sh .

# Lint + test + validate
make validate

# Smoke LinkML
bash herramientas/linkml/scripts/tests/smoke_sh.sh
```
