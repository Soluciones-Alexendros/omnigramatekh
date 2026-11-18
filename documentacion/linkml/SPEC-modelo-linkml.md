# Spec: modelo léxico y skill `linkml`

- **Estado:** vigente (revisada 2026-11-18 para alinearla con el ADR 0002)
- **Ámbito:** este repositorio. La skill vive en `herramientas/linkml/` y se
  llama `linkml`; no es un ramo del catálogo de `machineroom`.
- **Relacionados:** [ADR 0001](../adr/0001-sitio-estatico-aislado.md) (el sitio
  queda aislado del modelo), [ADR 0002](../adr/0002-incorporacion-herramientas-linkml.md)
  (la skill y el modelo viven aquí).

## Objective

Dotar al proyecto «Diagnosis y Actualización del Español-Castellano» de un
modelo léxico trazable y verificable: clases, slots, relaciones, vocabularios e
instancias YAML/JSON modeladas con LinkML, con validación por capas, generación
de artefactos (JSON Schema, Python/Pydantic, SQL, JSON-LD, SHACL, documentación)
y evolución versionada.

La skill `linkml` (en `herramientas/linkml/`) es el contrato operativo del
agente para ese ciclo. El modelo se especifica aquí; las decisiones de
modelado se toman en este repositorio, no en el catálogo de skills de la flota.

**Estado real, sin adornos:** el modelo **no está construido**. Lo que existe es
(a) la herramienta y su disciplina de verificación y (b) un laboratorio ficticio
(`herramientas/linkml/assets/schema-template.yaml`, con `Catalog`/`Source`/`Word`)
que demuestra el ciclo. Las 19 tablas y los validadores V01–V25 descritos abajo
son el **diseño de referencia** documentado en Notion, no código de este repo.

## Fuentes oficiales y reputadas

Verificadas el 2026-11-12. La skill las cita como referencia canónica y **nunca
afirma un comando, flag, versión o generador sin verificarlo** contra la
documentación oficial, el `--help` de la versión instalada o context7.

### Oficiales (primarias)

| #   | Fuente                        | URL                                                        | Qué aporta                                                                                                                      |
| --- | ----------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| F1  | Documentación oficial LinkML  | https://linkml.io/linkml/                                  | Tutoriales 1–9, schemas, working with data, generadores, CLI, FAQ, ecosystem                                                    |
| F2  | Repo de herramientas `linkml` | https://github.com/linkml/linkml                           | Código del CLI y generadores; PyPI `linkml` 1.12.1, Apache-2.0, Python ≥3.10                                                    |
| F3  | Metamodelo y especificación   | https://github.com/linkml/linkml-model                     | Metamodelo del lenguaje (ClassDefinition, SlotDefinition, etc.)                                                                 |
| F4  | Instalación oficial           | https://linkml.io/linkml/intro/install.html                | `pip install linkml` en venv; imagen OCI `docker.io/linkml/linkml`                                                              |
| F5  | CLI `linkml validate`         | https://linkml.io/linkml/cli/validate.html                 | `-s/--schema`, `-C/--target-class`, `--fix`, `--config`; sin `-s` valida contra el metamodelo                                   |
| F6  | CLI `linkml lint`             | https://linkml.io/linkml/cli/lint.html                     | Reglas de calidad del esquema, configuración, `--fix`                                                                           |
| F7  | CLI `linkml generate`         | https://linkml.io/linkml/generators/                       | Generadores: json-schema, python, pydantic, sqlddl, sqlalchemy, jsonld, shacl, owl, graphql, markdown, er-diagram, y otros      |
| F8  | Validación de datos           | https://linkml.io/linkml/data/validating-data.html         | Estrategias (runtime, JSON Schema, ShEx/SHACL) y límites de cobertura                                                           |
| F9  | Conversión de datos           | https://linkml.io/linkml/data/conversion.html              | `linkml-convert` (loaders/dumpers: JSON, YAML, RDF/Turtle, TSV/CSV)                                                             |
| F10 | Entrypoint `gen-project`      | https://linkml.io/linkml/generators/project-generator.html | Proyecto completo: `-d`, `-I/--include`, `-X/--exclude`, `-A/--generator-arguments`, `--mergeimports`                           |
| F11 | Ecosistema                    | https://linkml.io/linkml/ecosystem.html                    | linkml-runtime, linkml-map, linkml-store, schemasheets, schema-automator, linkml-owl, SSSOM, OAK, DataHarmonizer                |
| F12 | Repos de soporte              | https://github.com/linkml                                  | runtime, map, store, schemasheets, schema-automator                                                                             |
| F13 | Repos oficiales Arch          | https://archlinux.org/packages/                            | `python` (core, incluye `venv`) y `python-pip` (extra). Verificado el 2026-11-12                                                |
| F14 | AUR                           | https://aur.archlinux.org/                                 | **No existe** paquete `python-linkml` ni `linkml` en repos oficiales (verificado el 2026-11-12) → pip en venv es la vía en Arch |
| F15 | Arch Wiki · Python            | https://wiki.archlinux.org/title/Python                    | Recomienda venv aislado por proyecto; pip global no es vía soportada (PEP 668)                                                  |
| F16 | Metadatos PyPI `linkml`       | https://pypi.org/pypi/linkml/1.12.1/json                   | Sin extras; dependencias con wheels linux x86_64 (no requiere `base-devel`)                                                     |

### Verificación por contexto (context7)

- Documentación: `/websites/linkml_io_linkml`
- Repo: `/linkml/linkml`
- Metamodelo: `/linkml/linkml-model`

Uso: resolver la duda antes de afirmar que una API, flag o versión existe.

### Caso de referencia (lectura, Notion)

Proyecto «Diagnosis y Actualización del Español-Castellano»: esquema LinkML
1.12.1, 19 tablas, validadores V01–V25, adaptadores por fuente (BOE API REST,
Wikidata SPARQL, MediaWiki). Se usa como patrón en
`herramientas/linkml/references/project-integration.md`, sin acoplar la skill al
proyecto ni incorporar datos privados al repo.

## Tech Stack

- **Skill:** Markdown + frontmatter YAML. Vive en `herramientas/linkml/SKILL.md`.
- **Scripts:** Python 3 (stdlib) y Bash. Sin dependencias nuevas: la skill no
  instala LinkML por su cuenta, lo verifica y lo usa si está disponible.
- **Exit codes canónicos:** `0` OK · `1` error o veredicto negativo ·
  `2` input inválido · `3` dependencia ausente · `4` permiso.
- **Entorno de ejecución LinkML:** Python ≥3.10 con `pip install linkml` en venv
  aislado o imagen OCI `docker.io/linkml/linkml`. Versión fijada y registrada en
  cada ciclo; nunca instalación global no justificada.

### Instalación en Arch Linux — un solo script sobre venv

`herramientas/linkml/scripts/bootstrap_arch.sh` hace todo en una pasada
(dry-run por defecto; `--apply` ejecuta):

| Componente  | Origen                  | Elemento                                                               |
| ----------- | ----------------------- | ---------------------------------------------------------------------- |
| Sistema     | pacman (con sudo)       | `python` (core, incluye `venv`), `python-pip` (extra)                  |
| Aislamiento | `python -m venv`        | venv dedicado, parametrizable con `--venv-dir`                         |
| Librerías   | pip **dentro del venv** | `linkml==1.12.1` desde `assets/requirements-linkml.txt`                |
| Alternativa | Imagen OCI oficial      | `docker.io/linkml/linkml` (documentada, no instalada por el bootstrap) |

Razones verificadas: no hay paquete de LinkML en repos oficiales ni en AUR
(F14); Arch aplica PEP 668 y la Wiki recomienda venv por proyecto (F15).

```text
bootstrap_arch.sh [--apply] [--venv-dir DIR] [--skip-pacman] [--verify]
  default: dry-run (imprime el plan, no ejecuta nada)
  preflight: ¿Arch Linux? ¿pacman? ¿sudo? ¿python ≥3.10? ¿red hacia PyPI?
  1. pacman: python + python-pip (solo si faltan; con sudo y confirmación)
  2. venv: python -m venv <dir>; upgrade de pip dentro del venv
  3. pip: -r assets/requirements-linkml.txt (pin linkml==1.12.1)
  4. verificar: linkml --version + laboratorio con validate_cycle.py
  5. resumen: cómo activar el venv y próximos pasos
  idempotente; exit codes canónicos
```

## Project Structure

```text
herramientas/linkml/
├── SKILL.md                    # contrato de la skill (name: linkml)
├── references/                 # plano, sin subdirectorios
│   ├── installation.md
│   ├── ecosystem.md
│   ├── schema-authoring.md
│   ├── validation.md
│   ├── generators.md
│   ├── official-sources.md
│   └── project-integration.md
├── scripts/
│   ├── bootstrap_arch.sh
│   ├── linkml_env.py
│   ├── validate_cycle.py
│   └── tests/smoke_sh.sh
└── assets/
    ├── requirements-linkml.txt # pin linkml==1.12.1
    ├── schema-template.yaml    # laboratorio mínimo (Catalog/Source/Word)
    ├── instance-valid.yaml
    └── instance-invalid.yaml

documentacion/linkml/
├── SPEC-modelo-linkml.md       # este documento
└── MAPEO-entidades.md          # LinkML (canónico) ↔ SQL (proyección)
```

## Contenidos de la skill (mapa de conocimiento)

Procedimiento operativo en cinco fases, con la disciplina de verificación del
repo:

1. **Encuadrar.** Objetivo, consumidor, límites, datos reales de ejemplo,
   destinos, sensibilidad. Distinguir modelo conceptual → esquema → instancias →
   artefactos.
2. **Diseñar el dominio.** Entidades con identidad, relaciones y cardinalidad,
   ciclo de vida, anidado vs referencia por id, ausencia / desconocido / no
   aplicable, unidades y temporalidad, vocabularios cerrados solo si se conocen.
   Separar entidad / recurso / fuente / versión / ficha, y atribución de
   transcripción / inferencia.
3. **Escribir el esquema.** YAML con `id`, `name`, `prefixes`, `imports`
   (`linkml:types`), `classes`, `slots`; tipos, `required`, cardinalidad, rangos,
   enums; reutilizar slots por significado real; un `tree_root` si el formato lo
   necesita; al menos una instancia válida y una inválida por regla crítica.
4. **Verificar y generar.** Orden estricto: YAML → `linkml validate`
   (metamodelo) → `linkml lint` → `linkml validate -s -C` (instancia, positivo y
   negativo) → controles de dominio propios (unicidad, integridad referencial,
   procedencia). Generar solo lo necesario y probar el artefacto: no se asume
   equivalencia semántica entre generadores.
5. **Integrar y evolucionar.** Esquema canónico versionado y proyecciones;
   cambios compatibles vs rupturas, migración y rollback antes de tocar
   contratos; Notion y SQL como proyecciones con mapeo y pérdida semántica
   evaluada; minimizar exposición de datos sensibles.

**Restricciones de conducta:** no atribuir veracidad a un dato por cumplir un
esquema; no inventar comandos, flags ni versiones; no `--fix`, migraciones ni
sobrescrituras destructivas sin revisar alcance y autorización; no raspar
fuentes sin API por el hecho de no tenerla; no instalar dependencias globales.

## Commands

Validación del repo (no de la skill):

```bash
npm test                                  # checks T01–T09 del sitio
make validate                             # lint + test + estructura P1 + smoke LinkML
bash scripts/check-structure.sh . --profile P1
bash herramientas/linkml/scripts/tests/smoke_sh.sh
bash herramientas/linkml/scripts/bootstrap_arch.sh                  # dry-run
bash herramientas/linkml/scripts/bootstrap_arch.sh --apply --verify  # instala
python3 herramientas/linkml/scripts/linkml_env.py                    # ¿hay entorno?
```

## Testing Strategy

- **Validación estática del repo:** `scripts/check-structure.sh` (perfil P1) y
  Prettier. Ambos son gates reales: fallan si hay defecto.
- **Smoke de scripts LinkML:** `scripts/tests/smoke_sh.sh` ejecuta `--help` y
  `py_compile` de cada `.py`, y el dry-run del bootstrap. El dry-run del
  bootstrap solo se exige en Arch; en otros sistemas se registra como omitido.
- **Laboratorio funcional:** con `assets/`, el esquema pasa el metamodelo, el
  lint sale limpio, la instancia válida se acepta y la inválida se rechaza;
  opcionalmente se genera un artefacto (json-schema) y se comprueba. Se anota la
  versión de LinkML ejecutada.
- **Prueba de instalación real (Arch):** venv en ruta temporal, `linkml --version`
  correcto, laboratorio verde, segunda pasada idempotente.

## Boundaries

- **Always:** responder en español; verificar comandos contra la versión
  instalada y la documentación oficial; scripts deterministas con exit codes
  canónicos y salida estructurada; dry-run por defecto e idempotencia en el
  bootstrap.
- **Ask first:** cambiar el pin `linkml==1.12.1`; añadir dependencias al repo;
  modificar `scripts/check-structure.sh` (contrato P1) o el workflow de CI.
- **Never:** editar las páginas de Notion del proyecto (solo lectura); instalar
  LinkML globalmente; afirmar versiones o flags sin verificación; incluir datos
  privados del proyecto en la skill; acoplar `sitio/` al modelo (ADR 0001).

## Success Criteria

1. `scripts/check-structure.sh . --profile P1` en verde.
2. `bash herramientas/linkml/scripts/tests/smoke_sh.sh` en verde.
3. `SKILL.md` con frontmatter válido y referencias que existen.
4. Laboratorio funcional ejecutado y registrado, con la versión de LinkML usada.
5. Las 7 `references/` existen, son planas y enlazan solo a fuentes verificadas.
6. Ninguna página de Notion del proyecto modificada.
7. `sitio/` sigue sin leer ningún fichero de `herramientas/linkml/`.

## Open Questions

1. **¿Se construye ya el esquema real del modelo léxico?** Resuelto:
   no hasta formalizar el mapping de entidades (punto 2). Hoy solo existe el
   laboratorio ficticio; abrir el modelo sin mapping genera deuda de migración.
2. **¿Cuál es el vocabulario canónico de entidades?** Resuelto en cuanto al
   criterio: LinkML es el canon y las tablas SQL son proyección. Pero el
   inventario **no está cerrado**: el listado de 19 tablas y los ERD
   versionados discrepan en 10 entidades. [MAPEO-entidades.md](MAPEO-entidades.md)
   lo documenta (D1–D6) y fija el orden de resolución. No se inventan clases.
3. **¿Pin exacto `linkml==1.12.1` o rango `~=1.12`?** Propuesta: pin exacto.
   Reproducibilidad y la skill registra la versión realmente ejecutada.
4. **¿Ubicación por defecto del venv?** Resuelto: `~/Projects/linkml/venvs/linkml`,
   parametrizable con `--venv-dir`.
5. **¿El bootstrap instala `docker` como ruta OCI alternativa?** Propuesta: no;
   solo documentar la imagen `docker.io/linkml/linkml`.
6. **¿Idioma de la skill y sus referencias?** Resuelto: se mantiene en inglés
   como excepción declarada en `ARCHITECTURE.md` (convención del ecosistema
   LinkML), con la especificación del modelo en español.
