# Mapeo de entidades: LinkML (canónico) ↔ ERD ↔ listado SQL

### Propósito de este documento

Fija qué vocabulario es canónico y qué es proyección, y expone **todas** las
discrepancias entre las tres fuentes que hoy describen el mismo dominio:

1. **LinkML** — el canon (validado y generado). En este repo **no existe
   todavía ninguna clase real**: solo el laboratorio ficticio
   (`herramientas/linkml/assets/schema-template.yaml`, con `Catalog`/`Source`/`Word`).
2. **ERD versionados** — `.archify/erd-*/candidate.json`, 7 diagramas con
   entidades concretas.
3. **Listado de 19 tablas** — el diseño de referencia documentado en Notion y
   citado en `SPEC-modelo-linkml.md`.

Si hay discrepancia, manda el LinkML. Mientras no exista, manda este documento
como registro de la deuda.

---

## 1. Estado real, sin adornos

- Clases LinkML implementadas en el repo: **0**.
- Clases LinkML de diseño nombradas en el caso de referencia: **5**
  (`Fichero`, `Fuente`, `Palabra`, `Acepcion`, `Uso`).
- Entidades distintas en los ERD versionados: **23**.
- Entidades en el listado de 19 tablas: **19**.
- Entidades en común entre ERD y listado: **16**.
- Nombres que solo aparecen en el listado: **3**.
- Nombres que solo aparecen en los ERD: **7**.

Ninguna de las tres fuentes cubre el dominio completo. Esto no es un defecto a
disimular: es el trabajo pendiente.

---

## 2. Correspondencia

| Clase LinkML (diseño) | ERD (`.archify/`)    | Listado 19 tablas  | Estado                          |
| --------------------- | -------------------- | ------------------ | ------------------------------- |
| `Fichero`             | `DOCUMENTO`          | `DOCUMENTO`        | Diseño; sin esquema             |
| `Fuente`              | `RECURSO`            | `RECURSO`          | Diseño; sin esquema             |
| `Palabra`             | `PALABRA`            | `PALABRA`          | Diseño; sin esquema             |
| `Acepcion`            | `ACEPCION`           | `ACEPCION`         | Diseño; sin esquema             |
| `Uso`                 | **— (no existe)**    | `USO`              | Diseño; el ERD no lo representa |
| — (sin clase)         | `AGENTE`             | `AGENTE`           | Sin modelo                      |
| — (sin clase)         | `EDICION`            | `EDICION`          | Sin modelo                      |
| — (sin clase)         | `CAPTURA`            | `CAPTURA`          | Sin modelo                      |
| — (sin clase)         | `SECCION`            | `SECCION`          | Sin modelo                      |
| — (sin clase)         | `ASERCION`           | `ASERCION`         | Sin modelo                      |
| — (sin clase)         | `REVISION`           | `REVISION`         | Sin modelo                      |
| — (sin clase)         | `GLOSARIO`           | `GLOSARIO`         | Sin modelo                      |
| — (sin clase)         | `GLOSARIO_PALABRA`   | `GLOSARIO_PALABRA` | Sin modelo                      |
| — (sin clase)         | `CORRESPONDENCIA`    | `CORRESPONDENCIA`  | Sin modelo                      |
| — (sin clase)         | `TAREA`              | `TAREA`            | Sin modelo                      |
| — (sin clase)         | `ENCABEZADO_CAMPO`   | `ENCABEZADO_CAMPO` | Sin modelo                      |
| — (sin clase)         | `REFERENCIA`         | `REFERENCIA`       | Sin modelo                      |
| — (sin clase)         | — (no existe)        | `ATESTIGUACION`    | Solo en el listado              |
| — (sin clase)         | — (no existe)        | `ORDEN`            | Solo en el listado              |
| — (sin clase)         | `EVIDENCIA`          | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `ORDEN_ACEPCION`     | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `UNIDAD_PLURIVERBAL` | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `SUPERIOR`           | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `MIEMBRO_GRUPO`      | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `COSTE`              | — (no existe)      | Solo en los ERD                 |
| — (sin clase)         | `ESTADO_DATO_CAMPO`  | — (no existe)      | Solo en los ERD                 |

---

## 3. Discrepancias que hay que resolver antes de escribir el esquema

| #   | Discrepancia                  | Detalle                                                                                                        | Decisión propuesta                                                          |
| --- | ----------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| D1  | `USO` sin ERD                 | Es una de las 5 clases de diseño, pero ningún diagrama la representa                                           | Decidir si `Uso` es entidad propia o vocabulario de `Acepcion`              |
| D2  | `ATESTIGUACION` huérfana      | En el listado, en ningún ERD ni clase                                                                          | Confirmar si es `EVIDENCIA` con otro nombre                                 |
| D3  | `ORDEN` vs `ORDEN_ACEPCION`   | Nombres distintos para el mismo rol                                                                            | Unificar; `ORDEN_ACEPCION` es más preciso                                   |
| D4  | `EVIDENCIA` fuera del listado | Aparece en `erd-evidencia` y no en las 19 tablas                                                               | Añadir al listado o absorber en `ATESTIGUACION`                             |
| D5  | 7 entidades solo en ERD       | `UNIDAD_PLURIVERBAL`, `SUPERIOR`, `MIEMBRO_GRUPO`, `COSTE`, `ESTADO_DATO_CAMPO`, `ORDEN_ACEPCION`, `EVIDENCIA` | Confirmar si son de dominio o de complemento operativo                      |
| D6  | `Fichero` vs `DOCUMENTO`      | El ERD y el listado usan `DOCUMENTO`; la clase de diseño, `Fichero`                                            | Mantener `Fichero` como clase y `DOCUMENTO` como nombre de tabla proyectada |

**Anterior versión de este documento** listaba `Uso` sin señalar la discrepancia
D1 y no incluía `ATESTIGUACION`, `ORDEN`, `EVIDENCIA`, `ORDEN_ACEPCION`,
`UNIDAD_PLURIVERBAL`, `SUPERIOR`, `MIEMBRO_GRUPO`, `COSTE` ni
`ESTADO_DATO_CAMPO`. Se corrige aquí; no se inventaron clases para ellas.

---

## 4. Convenciones de modelado

1. **El LinkML manda.** Si discrepa de una tabla SQL o de un ERD, se adaptan
   ellos (son proyección).
2. **Identidad.** Cada clase LinkML lleva `identifier: true` en su slot clave
   (`<entidad>_id`). Las tablas usan `*_id` como PK.
3. **Referencias.** LinkML: `range: OtraClase`. SQL: FK `*_id REFERENCES`.
4. **Cardinalidad.** `multivalued: true` → tabla puente o FK inversa según el
   patrón de acceso real, no por comodidad.
5. **Ausencia / Desconocido / No aplicable.** LinkML: `required: false` con
   `description` explícita. SQL: `NULL` más una columna de estado cuando la
   distinción importe (`ESTADO_DATO_CAMPO` ya apunta en esa dirección).

---

## 5. Próximos pasos

1. Resolver D1–D6 en un ADR nuevo (`documentacion/adr/0003-vocabulario-entidades.md`).
2. Escribir el esquema real en `herramientas/linkml/assets/schema.yaml`
   (sustituyendo el laboratorio como canon) con las clases acordadas.
3. Generar y comprobar artefactos: JSON Schema, Pydantic, SQL DDL.
4. Validar round-trip: YAML ↔ JSON ↔ SQL ↔ JSON-LD.
5. Regenerar los ERD desde el esquema, no a mano, para que no vuelvan a divergir.

---

## 6. Referencias

- [SPEC-modelo-linkml.md](SPEC-modelo-linkml.md) — especificación del modelo y la skill
- [ADR 0002](../adr/0002-incorporacion-herramientas-linkml.md) — ubicación de la herramienta
- [project-integration.md](../../herramientas/linkml/references/project-integration.md) — reglas de proyección
