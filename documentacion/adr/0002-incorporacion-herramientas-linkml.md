# ADR 0002 · Incorporación de las herramientas LinkML

- **Estado:** aceptado
- **Fecha:** 2026-11-17
- **Contexto:** PR #70 de `Soluciones-Alexendros/machineroom` (skill `data-linkml`), ADR 0001 de este repo

## Contexto

El modelo léxico de OmniGramatekh se describió desde el principio como un árbol
LinkML futuro (`esquema/`, `controles/`, `proyecciones/`, `ejemplos/`,
`historico/`), pero en este repositorio no existía ni el modelo ni la
herramienta para construirlo. El ADR 0001 solo decidió que el sitio estático de
`sitio/` queda aislado de cualquier módulo LinkML; no decidió dónde vive el
modelo.

Mientras tanto, la skill `data-linkml` se escribió como propuesta de catálogo en
`machineroom` (PR #70): autoría de esquemas, validación por capas, generación de
artefactos, bootstrap de entorno y referencias oficiales. Ese PR no podía
entrar en `machineroom` porque su taxonomía de dominios es un conjunto cerrado
(`plan`, `local`, `project`, `web`, `role`) y `data` no forma parte de él; además
introducía una familia de skills de un dominio técnico ajeno al producto.

## Decisión

1. La skill, sus referencias, sus scripts y sus activos de ejemplo viven en este
   repositorio, bajo `herramientas/linkml/`:
   - `herramientas/linkml/SKILL.md` — contrato de la skill (`name: linkml`).
   - `herramientas/linkml/references/` — instalación, ecosistema, autoría de
     esquemas, validación, generadores, fuentes oficiales e integración.
   - `herramientas/linkml/scripts/` — `bootstrap_arch.sh`, `linkml_env.py`,
     `validate_cycle.py` y su smoke.
   - `herramientas/linkml/assets/` — plantilla de esquema e instancias válida e
     inválida.
2. El modelo se especifica en `documentacion/linkml/SPEC-modelo-linkml.md`; las
   decisiones de modelo se toman aquí, no en `machineroom`.
3. `sitio/` sigue aislado (ADR 0001). Ningún fichero de `herramientas/linkml/` se
   lee desde la vista previa.
4. `machineroom` no incorpora la skill. Su PR #70 se cierra y el catálogo
   permanece en 14 skills con cinco dominios.

## Consecuencias

- El árbol de modelado tiene un único dueño: este repositorio. Un cambio de
  esquema no requiere tocar el catálogo de skills de la flota.
- La skill queda disponible para agentes desde este repo (`herramientas/linkml/`)
  aunque no se instalará como parte del catálogo de `machineroom`.
- `herramientas/linkml/assets/requirements-linkml.txt` fija `linkml==1.12.1`; un
  cambio de versión exige revalidar `validate_cycle.py` contra los casos de
  ejemplo antes de actualizar el pin.
- El smoke de las herramientas (`scripts/tests/smoke_sh.sh`) no entra en el gate
  de `npm test` de la vista previa: se ejecuta explícitamente. Si se incorpora al
  gate, debe seguir siendo read-only y sin red.

## Alternativas consideradas

- **Mantener la skill en `machineroom` con dominio `data`.** Rechazada: rompe un
  conjunto cerrado de dominios y mete en el producto una familia técnica que no
  le corresponde.
- **Dejar la skill en el PR #70 sin destino.** Rechazada: trabajo verificado
  (1.722 líneas, smoke en verde) que se pierde por no tener dueño.
- **Ponerla dentro de `sitio/`.** Rechazada: contradice ADR 0001 y expone
  material experimental en la superficie pública.

## Relacionados

- [ADR 0001](0001-sitio-estatico-aislado.md) — sitio estático aislado.
- `documentacion/linkml/SPEC-modelo-linkml.md` — especificación del modelo.
- `Soluciones-Alexendros/machineroom` PR #70 — origen del material.
