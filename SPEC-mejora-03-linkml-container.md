# Spec: MEJORA-03 — Entorno LinkML reproducible sin Arch

> Origen: auditoría crítica, MEJORA-03. Estado: en ejecución.

## Objective

Que el ciclo LinkML se ejecute igual en el portátil, en CI y en cualquier host,
sin depender de Arch ni de un `pip install` de 91 paquetes en el host:

- **Contenedor OCI** con la imagen oficial `linkml/linkml` **fijada por digest**
  (manifest list multi-arch), repo montado en solo lectura.
- `make validate-linkml` **prefiere contenedor** y cae al venv local si Docker no
  está disponible (sin romper el gate en portátiles sin Docker).
- **CI ejecuta el contenedor de verdad**, lo que convierte la reproducibilidad en
  algo verificado y no declarado.

## Decisión de diseño

| Opción                      | Descartada por                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Solo venv (actual)          | Depende de la distro/Python del host; 91 paquetes sin `--require-hashes` en el bootstrap antes de la fase anterior |
| Solo contenedor             | Rompe el gate en hosts sin Docker y en macOS sin daemon                                                            |
| **Contenedor con fallback** | Elegida: reproducible donde hay Docker, nunca bloquea donde no lo hay                                              |

## Contrato de exit codes

| Código | Significado                                                               |
| ------ | ------------------------------------------------------------------------- |
| 0      | ciclo PASS dentro del contenedor                                          |
| 1      | ciclo FAIL (se propaga el veredicto)                                      |
| 2      | input inválido (opción desconocida, assets ausentes)                      |
| 3      | Docker no disponible o daemon inaccesible → **el llamador hace fallback** |
| 4      | permiso (reservado, igual que en los scripts Python)                      |

## Commands

```bash
# Contenedor (imagen fijada por digest)
bash herramientas/linkml/scripts/validate_cycle_container.sh

# Gate completo con fallback automático
make validate-linkml

# Tests del wrapper con un docker falso (sin Docker real ni red)
.venv/bin/python -m pytest herramientas/linkml/scripts/tests/test_container_wrapper.py -v
```

## Project Structure

```
herramientas/linkml/scripts/
├── validate_cycle_container.sh        # wrapper OCI (nuevo)
└── tests/test_container_wrapper.py    # 6 tests con docker de mentira (nuevo)
```

## Testing Strategy

- **Unitaria (local, verificada)**: docker falso en `PATH` que registra sus
  argumentos → comprueba montaje `:ro`, digest en la imagen, propagación de
  exit codes 0/1/2/3 y override por `LINKML_IMAGE`.
- **Integración real (CI)**: job `linkml-container` ejecuta el wrapper contra la
  imagen real; es la única verificación válida de la imagen.
- **Fallback**: `make validate-linkml` en host sin Docker → smoke del venv.

## Boundaries

- Always: pin por **digest**, montaje `:ro`, no escribir en el host.
- Ask first: cambiar la imagen o el digest.
- Never: usar `:latest`; dar por verificado un contenedor sin ejecutarlo.

## Success Criteria

1. `validate_cycle_container.sh` devuelve 3 (no 1) cuando Docker no sirve.
2. `make validate-linkml` pasa en host sin Docker (fallback) **y** en CI con Docker.
3. CI ejecuta `pytest` de las herramientas (antes no se ejecutaba).
4. Job `linkml-container` verde ejecutando el ciclo real en el contenedor.

## Open Questions

- Ninguna abierta. La verificación en contenedor no puede hacerse en este host
  (socket de Docker sin permisos); se delega en CI y se documenta así.
