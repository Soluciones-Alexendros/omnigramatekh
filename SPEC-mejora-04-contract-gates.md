# Spec: MEJORA-04 — Gates de contrato, no de presencia

> Origen: auditoría crítica, MEJORA-04. Estado: en ejecución.

## Objective

Que el verde signifique **coherencia**, no existencia. `check-structure.sh` ya
comprueba que los ficheros están; este gate comprueba que lo que hay **concuerda
entre sí** y que los jobs de CI **hacen algo**.

Contratos implementados (`scripts/check_contracts.py`):

| Id  | Contrato                                                             | Fallo que detecta                                  |
| --- | -------------------------------------------------------------------- | -------------------------------------------------- |
| C1  | `package.json` versión == primera entrada de `CHANGELOG`             | release a medias, olvido de CHANGELOG              |
| C2  | Si `README` declara versión, coincide                                | README desactualizado tras release                 |
| C3  | Cada job de CI tiene un `run:` no trivial o un `uses:`               | job vaciado a `run: "true"` (pasaba desapercibido) |
| C4  | Cada directorio enlazado desde `docs/README.md` tiene contenido real | puertas a habitaciones vacías (D-014)              |
| C5  | Todo `uses:` está fijado por SHA de 40 hex                           | tag móvil reintroducido (deriva de D-009)          |

## Decisión de diseño

- **Sin PyYAML**: el parseo de workflows es conservador (solo lo que los
  contratos necesitan). Evita añadir dependencia a un gate que debe correr en
  cualquier host y en el job sin Python configurado.
- **Delimitación explícita**: `workflow_jobs()` solo lee bajo `jobs:`; las claves
  de 2 espacios de `on:` no se cuentan como jobs (bug real encontrado y
  corregido durante la implementación, con test de regresión).
- **Comandos triviales**: `run: true`, `:`, `exit 0`, `echo` no cuentan como
  ejecución real.

## Commands

```bash
make validate-contracts          # gate (incluido en make validate)
python3 scripts/check_contracts.py --root DIR   # contra otra raíz
.venv/bin/python -m pytest scripts/tests -v     # 9 tests negativos
```

## Project Structure

```
scripts/
├── check_contracts.py           # nuevo gate (C1–C5)
└── tests/test_check_contracts.py # un caso negativo por contrato + regresión
```

## Testing Strategy

- **Un caso negativo por contrato** con repos mínimos en `tmp_path` (C1 dos
  variantes, C2, C3, C4, C5) — el gate se prueba contra el fallo, no contra el
  repo sano.
- **Regresión**: `test_no_confunde_on_con_jobs` fija el bug de parseo.
- **Positivo**: `make validate-contracts` sobre el repo real → 0 incumplimientos.
- CI ejecuta el gate (job `validate-structure`) y la suite pytest completa.

## Boundaries

- Always: un contrato nuevo entra con su test negativo.
- Ask first: endurecer un contrato que hoy pasa (p. ej. exigir PR template).
- Never: relajar un contrato para que pase un cambio; se corrige el cambio.

## Success Criteria

1. `make validate-contracts` → exit 0 en el repo; exit 1 con cualquier contrato roto.
2. 9 tests negativos en verde; el bug de parseo de `on:` cubierto.
3. El gate forma parte de `make validate` y del CI.
4. Documentado qué detecta cada contrato (esta spec + `make help`).
