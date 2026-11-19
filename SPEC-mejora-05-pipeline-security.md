# Spec: MEJORA-05 — Seguridad de pipeline desde el commit

> Origen: auditoría crítica, MEJORA-05. Estado: en ejecución.

## Objective

Automatizar la defensa de la cadena de suministro y la higiene de workflows, que
hasta ahora dependía de una revisión manual:

- **zizmor** (auditoría de seguridad de workflows) y **actionlint** (sintaxis con
  semántica de expresiones) como gate, con versiones fijadas.
- **OpenSSF Scorecard** semanal + SARIF a code scanning.
- Los hallazgos que aparezcan se corrigen, no se silencian.

## Hallazgos reales encontrados y corregidos al activar zizmor

| Regla           | Hallazgo                                                                       | Corrección                            |
| --------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| `artipacked`    | 8 checkouts persistían credenciales en `.git/config`, exportables a artefactos | `persist-credentials: false` en los 8 |
| `unpinned-uses` | `github/codeql-action/upload-sarif@v3` (tag móvil)                             | fijado por SHA de commit              |

Resultado tras corregir: **0 hallazgos**.

## Commands

```bash
make validate-workflows          # actionlint + zizmor
zizmor --persona=regular .github/workflows/
actionlint .github/workflows/*.yml
```

## Project Structure

```
.github/workflows/
├── ci.yml            # + gate actionlint/zizmor (versiones fijadas)
└── scorecard.yml     # nuevo: semanal, SARIF a code scanning
```

## Testing Strategy

- Positivo local: `make validate-workflows` en verde sobre 2 workflows.
- Negativo local: reintroducir un `uses: @v3` y un checkout sin
  `persist-credentials` → zizmor debe fallar (high) y actionlint seguir pasando.
- CI: el step forma parte del job `quality`, que ya es obligatorio.

## Boundaries

- Always: pin de linters y actions; corregir el hallazgo, no añadir `# zizmor: ignore`.
- Ask first: `publish_results: true` en Scorecard (publica metadatos del repo).
- Never: `@latest` en herramientas de seguridad; permisos `write-all`.

## Success Criteria

1. `zizmor` sin hallazgos y `actionlint` limpio sobre los 2 workflows.
2. CI ejecuta ambos en cada PR.
3. Scorecard programado semanalmente, subiendo SARIF.
4. Test negativo demuestra que el gate falla si se reintroduce el patrón.
