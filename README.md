# OmniGramatekh

Diagnosis y Actualización del Español-Castellano. Repositorio de trabajo experimental.

## Vista previa local

La portada estática vive en `sitio/`. No es un sitio publicado.

```bash
cd sitio && python3 -m http.server 8765 --bind 127.0.0.1
```

Pruebas locales:

```bash
npm test
# o: python3 sitio/pruebas/run_checks.py
```

## Planos Archify

Diagramas HTML autónomos en `.archify/` (arquitectura, flujo, árbol y entidades). Describen la vista previa real y el diseño documental de Notion; el modelo LinkML no está construido en este árbol.

## Límites

Sin despliegue, sin acoplamiento a Notion ni a módulos LinkML en la portada. Ver `documentacion/adr/0001-sitio-estatico-aislado.md`.
