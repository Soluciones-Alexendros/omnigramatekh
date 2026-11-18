# Mapeo de entidades: LinkML (canónico) ↔ SQL (proyección Notion)

### Propósito de este documento

Fija la correspondencia explícita entre el vocabulario **canónico** del modelo
LinkML (PascalCase, validado y generado) y las **19 tablas SQL** en mayúscula
que documenta el caso de referencia de Notion (proyección, no canon).

Si una tabla no tiene clase LinkML todavía, queda marcada como **PENDIENTE**.
Si una clase LinkML no tiene tabla SQL, se marca como **INTERNA** (solo existe
en el modelo para validación o generación).

---

## Tabla de correspondencia

| LinkML (canónico) | SQL (Notion)       | Estado      | Notas                                                                  |
| ----------------- | ------------------ | ----------- | ---------------------------------------------------------------------- |
| `Fichero`         | `DOCUMENTO`        | PENDIENTE   | Clase base del laboratorio; en Notion parte de `DOCUMENTO` + `SECCION` |
| `Fuente`          | `RECURSO`          | PENDIENTE   | En Notion: `RECURSO` + `EDICION` + `CAPTURA`                           |
| `Palabra`         | `PALABRA`          | PENDIENTE   | Corresponde 1:1 en concepto; falta esquema LinkML real                 |
| `Acepcion`        | `ACEPCION`         | PENDIENTE   | Idem                                                                   |
| `Uso`             | `USO`              | PENDIENTE   | Idem                                                                   |
| `Agente`          | `AGENTE`           | PENDIENTE   | No existe en laboratorio actual                                        |
| `Edicion`         | `EDICION`          | PENDIENTE   | Se modela como atributo de `Fuente` en laboratorio                     |
| `Captura`         | `CAPTURA`          | PENDIENTE   | No existe en laboratorio actual                                        |
| `Asercion`        | `ASERCION`         | PENDIENTE   | No existe en laboratorio actual                                        |
| `Seccion`         | `SECCION`          | PENDIENTE   | No existe en laboratorio actual                                        |
| `Evidencia`       | `EVIDENCIA`        | PENDIENTE   | No existe en laboratorio actual                                        |
| `Revision`        | `REVISION`         | PENDIENTE   | No existe en laboratorio actual                                        |
| `Glosario`        | `GLOSARIO`         | PENDIENTE   | No existe en laboratorio actual                                        |
| `GlosarioPalabra` | `GLOSARIO_PALABRA` | PENDIENTE   | No existe en laboratorio actual                                        |
| `Correspondencia` | `CORRESPONDENCIA`  | PENDIENTE   | No existe en laboratorio actual                                        |
| `Tarea`           | `TAREA`            | PENDIENTE   | No existe en laboratorio actual                                        |
| `EncabezadoCampo` | `ENCABEZADO_CAMPO` | PENDIENTE   | No existe en laboratorio actual                                        |
| `Referencia`      | `REFERENCIA`       | PENDIENTE   | No existe en laboratorio actual                                        |
| `Catalogo`        | _(raíz)_           | **INTERNA** | Solo `tree_root` del laboratorio; no tiene tabla SQL                   |

---

## Convenciones de modelado

1. **El LinkML manda**: si hay discrepancia, el esquema LinkML es la fuente de
   verdad y la tabla SQL se adapta (proyección).
2. **Identidad**: cada clase LinkML tiene `identifier: true` en su slot clave
   (p.ej. `palabra_id`). Las tablas SQL usan `*_id` como PK.
3. **Referencias**: en LinkML son `range: OtraClase` + `inlined: false`; en SQL
   son FK (`*_id REFERENCES otra_tabla(*_id)`).
4. **Cardinalidad**: `multivalued: true` → tabla puente o FK inversa; en SQL se
   materializa según patrón de acceso.
5. **Ausencia / Desconocido / No Aplicable**: se modela en LinkML con
   `required: false` + `description` explícita; en SQL con `NULL` + `CHECK`
   o columna de estado.

---

## Próximos pasos

1. Escribir el esquema real en `herramientas/linkml/assets/schema.yaml`
   (reemplazando `schema-template.yaml` como canon).
2. Generar artefactos: JSON Schema, Pydantic, SQL DDL (`linkml generate`).
3. Validar round-trip: instancias YAML ↔ JSON ↔ SQL ↔ JSON-LD.
4. Este documento se actualiza en el mismo PR que el esquema.

---

## Referencias

- [SPEC-modelo-linkml.md](../linkml/SPEC-modelo-linkml.md) — especificación del modelo y la skill
- [ADR 0002](../../adr/0002-incorporacion-herramientas-linkml.md) — decisión de ubicación
- [project-integration.md](../references/project-integration.md) — reglas de proyección
