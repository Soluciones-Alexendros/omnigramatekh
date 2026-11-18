# Documentación — omnigramatekh

### Propósito de este documento

Es el índice de la documentación **de uso** del repositorio y delimita dos
árboles que no deben confundirse: `docs/` (guías para quien usa o modifica el
proyecto) y `documentacion/` (canon técnico: ADRs y especificaciones).

---

## Dos árboles, dos propósitos

| Árbol            | Qué contiene                                           | Quién lo lee                     | Cambia cuando                          |
| ---------------- | ------------------------------------------------------ | -------------------------------- | -------------------------------------- |
| `docs/`          | Guías de uso, arquitectura explicada, procedimientos   | Quien usa o mantiene el proyecto | Cambia una práctica o un guía          |
| `documentacion/` | ADRs, especificaciones de modelo, decisiones con fecha | Quien decide o audita            | Se toma una decisión o cambia el canon |

`docs/` **no es el canon**: si una guía contradice un ADR de `documentacion/`,
manda el ADR y la guía está mal y hay que corregirla.

## Estructura

```
docs/
├── architecture/   # Visión técnica explicada (complementa ARCHITECTURE.md)
├── guides/         # Cómo usar, desarrollar y contribuir
└── runbooks/       # Procedimientos: reproducir, diagnosticar, recuperar
```

## Acceso rápido

| Directorio                     | Contenido                                 | Audiencia                    |
| ------------------------------ | ----------------------------------------- | ---------------------------- |
| [architecture/](architecture/) | Diagramas de capas, decisiones explicadas | Desarrolladores, arquitectos |
| [guides/](guides/)             | Cómo desarrollar, testear, contribuir     | Contribuyentes               |
| [runbooks/](runbooks/)         | Procedimientos y troubleshooting          | Maintainers                  |

## Canon técnico (fuera de `docs/`)

| Archivo                                      | Descripción                                    |
| -------------------------------------------- | ---------------------------------------------- |
| `ARCHITECTURE.md`                            | Arquitectura actual, en la raíz del repo       |
| `documentacion/adr/`                         | Architecture Decision Records                  |
| `documentacion/linkml/SPEC-modelo-linkml.md` | Especificación del modelo léxico y de la skill |
| `documentacion/linkml/MAPEO-entidades.md`    | LinkML (canónico) ↔ SQL (proyección)           |
| `CONTRIBUTING.md`                            | Guía de contribución                           |
| `SECURITY.md`                                | Política de seguridad                          |
| `CHANGELOG.md`                               | Historial de cambios                           |
| `.archify/`                                  | Diagramas HTML autónomos (artefacto y fuente)  |

## Convenciones

- **Formato:** Markdown con Prettier (gate `make validate-docs`).
- **Nombrado:** kebab-case para archivos (`mi-guia.md`).
- **Meta-sección:** cada documento de este árbol incluye
  `### Propósito de este documento` al inicio.
- **Sincronía:** una guía cambia en el mismo PR que la práctica que describe.
- **Diagramas:** el artefacto es el `.html` de `.archify/`; su fuente es el
  `candidate.json` del mismo directorio. Ambos se versionan; los recibos
  intermedios no.
