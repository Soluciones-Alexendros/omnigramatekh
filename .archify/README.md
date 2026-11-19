# Diagramas .archify — Canon de generación

> **Generación canónica (vigente): timestamp `20261113-112344`**
>
> Los diagramas con timestamp `20261113-111148` son generaciones previas
> superadas y **no deben usarse como referencia**.

## Lista de diagramas canónicos (20261113-112344)

| Diagrama | Descripción | Archivo HTML |
|----------|-------------|--------------|
| architecture-capas | Arquitectura por capas (C4 nivel 1-2) | `architecture-capas-20261113-112344/index.html` |
| architecture-vista-previa | Vista previa de arquitectura | `architecture-vista-previa-20261113-112344/index.html` |
| erd-aserciones | ERD: Aserciones y validaciones | `erd-aserciones-20261113-112344/index.html` |
| erd-complemento | ERD: Complemento léxico | `erd-complemento-20261113-112344/index.html` |
| erd-curacion | ERD: Proceso de curación | `erd-curacion-20261113-112344/index.html` |
| erd-documentos | ERD: Documentos y fuentes | `erd-documentos-20261113-112344/index.html` |
| erd-evidencia | ERD: Evidencia y trazabilidad | `erd-evidencia-20261113-112344/index.html` |
| erd-fuentes | ERD: Fuentes y procedencia | `erd-fuentes-20261113-112344/index.html` |
| erd-lexico | ERD: Léxico y formulaciones | `erd-lexico-20261113-112344/index.html` |
| tree-componentes | Árbol de componentes del sistema | `tree-componentes-20261113-112344/index.html` |
| workflow-flujo-palabra | Flujo de trabajo: ciclo de vida de una palabra | `workflow-flujo-palabra-20261113-112344/index.html` |

## Generaciones superadas (NO USAR)

- `architecture-vista-previa-20261113-111148/` — versión previa de vista previa
- `tree-componentes-20261113-111148/` — versión previa de árbol de componentes

## Regeneración

Los diagramas se generan desde `candidate.json` usando archify. Para regenerar:

```bash
# Requiere archify CLI instalado
archify generate --input candidate.json --output .archify/<nombre>-<timestamp>/
```

**Política**: Solo los `candidate.json` y sus HTML canónicos se versionan.
Las generaciones intermedias y receipts NO se versionan.