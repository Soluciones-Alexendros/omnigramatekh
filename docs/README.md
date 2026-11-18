# Documentación — omnigramatekh

Índice de navegación de la documentación de usuario.

## Estructura

```
docs/
├── architecture/   # Decisiones arquitectónicas, diagramas, visión técnica
├── guides/         # Guías de uso, desarrollo, contribución
└── runbooks/       # Procedimientos operativos, troubleshooting
```

## Acceso rápido

| Directorio                     | Contenido                                    | Audiencia                       |
| ------------------------------ | -------------------------------------------- | ------------------------------- |
| [architecture/](architecture/) | ADRs, diagramas Archify, visión técnica      | Desarrolladores, Arquitectos    |
| [guides/](guides/)             | Cómo desarrollar, testear, contribuir        | Contribuyentes, Desarrolladores |
| [runbooks/](runbooks/)         | Procedimientos, troubleshooting, operaciones | Maintainers, On-call            |

## Documentación relacionada (fuera de `docs/`)

| Archivo                 | Descripción                   |
| ----------------------- | ----------------------------- |
| `README.md`             | Visión general del proyecto   |
| `ARCHITECTURE.md`       | Arquitectura actual detallada |
| `CONTRIBUTING.md`       | Guía de contribución          |
| `SECURITY.md`           | Política de seguridad         |
| `CHANGELOG.md`          | Historial de cambios          |
| `documentacion/adr/`    | Architecture Decision Records |
| `documentacion/linkml/` | Especificación modelo LinkML  |
| `.archify/`             | Diagramas HTML autónomos      |

## Convenciones

- **Formato**: Markdown (Prettier, headings ATX)
- **Nombrado**: kebab-case para archivos (`mi-guia.md`)
- **Meta-sección**: Cada doc incluye `### Propósito de este documento` al inicio
- **Actualización**: Docs cambian en el mismo PR que el código que documentan
