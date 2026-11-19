# Spec: MEJORA-02 — Validadores como producto (suite y lint de shell)

> Origen: auditoría crítica, MEJORA-02. Estado: **parcialmente implementado**
> (ver «Límite conocido»).

## Objective

Que los validadores del repo tengan una suite que ejerza sus **fallos**, no solo
su `--help`, y que el código de shell pase un linter real.

## Implementado

| Pieza                                   | Qué cubre                                                                                                 |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `herramientas/linkml/scripts/tests/`    | 21 tests: `validate_cycle` (5), `linkml_env` (4), bootstrap (6), wrapper de contenedor (6)                |
| `scripts/tests/test_check_contracts.py` | 9 tests: un caso negativo por contrato C1–C5 + regresión de parseo                                        |
| `scripts/tests/test_common.py`          | 12 tests **directos** de `_common.py`: `find_linkml` (5), `verify_executable` (4), `run` + exit codes (3) |
| `shellcheck` en `make lint` y CI        | `.sh` de herramientas, `scripts/` y hooks, versión fijada `shellcheck-py==0.11.0.1`                       |
| CI                                      | `pytest -q` con los `testpaths` de `pyproject.toml` (42 tests)                                            |

Total: **42 tests**, todos con camino de error explícito; 0 dependientes de estar
en Arch, con Docker o con `linkml` instalado (se omiten si falta el binario).

### Hallazgos reales corregidos al activar shellcheck

| Aviso    | Dónde                         | Corrección                                         |
| -------- | ----------------------------- | -------------------------------------------------- |
| `SC2034` | `validate_cycle_container.sh` | variable `ASSETS` sin usar (residuo) eliminada     |
| `SC2043` | `check-structure.sh`          | bucle `for dep in grep` de un solo elemento → `if` |
| `SC2154` | `check-structure.sh`          | `rc` referenciado en el `trap` → `$?` directo      |

## Límite conocido (no implementado, y por qué)

**Pruebas de mutación** (`mutmut`) sobre `scripts/_common.py`: intentadas y
**bloqueadas por la herramienta**, no por falta de tests.

- Con los tests vía subprocess: «could not find any test case for any mutant»
  (sin import directo no hay mapeo de cobertura).
- Añadidos 12 tests **directos** (valor real, se quedan): mutmut entonces falla
  con «tests recorded trampoline hits but none match any mutant key» — exige
  imports de paquete (`scripts._common`) con `scripts/` como paquete, lo que
  rompería el layout plano de scripts y su uso como ejecutables.

Se prefiere no deformar el layout del repo para satisfacer a una herramienta, y
no se declara una métrica de mutación que no se ha podido verificar.

Aviso operativo: al ejecutarse, mutmut **reescribe los ficheros fuente** para
instrumentarlos (en la prueba: +31.201 líneas en `_common.py`, con `.meta` y
`.spans`). Se restauró con `git checkout` y se verificó después (42 tests y
`make validate` en verde). Motivo adicional para no integrarlo en el flujo:
toca el árbol de trabajo de forma invasiva.

## Commands

```bash
.venv/bin/python -m pytest -q                 # 42 tests
make lint                                     # prettier + ruff + shellcheck
```

## Boundaries

- Always: un validador nuevo entra con sus caminos de error cubiertos.
- Ask first: introducir un runner de mutación que exija cambiar el layout.
- Never: declarar cobertura de mutación sin haberla medido.

## Success Criteria

1. `pytest -q` → 42 tests, 0 fallos, en cualquier host (skips donde falte binario). ✅
2. `shellcheck -S warning` limpio sobre todos los `.sh` y hooks. ✅
3. CI ejecuta ambos. ✅
4. Mutación: **documentada como no viable** con el layout actual. ⚠️
