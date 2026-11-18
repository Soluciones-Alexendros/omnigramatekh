# OmniGramatekh

### Propósito de este documento

Portada del repositorio: describe qué es OmniGramatekh (diagnóstico y actualización del español-castellano, repo experimental), cómo previsualizar el sitio estático local, cómo ejecutar pruebas, dónde están los diagramas Archify, las herramientas LinkML, y los límites del proyecto (sin despliegue, sin acoplamiento a Notion).

---

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

Diagramas HTML autónomos en `.archify/` (arquitectura, flujo, árbol y entidades). Describen la vista previa real y el diseño documental de Notion; el modelo LinkML no está construido todavía.

## Herramientas LinkML

`herramientas/linkml/` contiene la skill de modelado, sus referencias, el
bootstrap de entorno y los validadores del modelo léxico:

```bash
bash herramientas/linkml/scripts/tests/smoke_sh.sh   # smoke read-only
python3 herramientas/linkml/scripts/linkml_env.py     # ¿hay entorno LinkML?
```

Especificación del modelo: `documentacion/linkml/SPEC-modelo-linkml.md`.
Decisiones: [ADR 0002](documentacion/adr/0002-incorporacion-herramientas-linkml.md).

## Límites

Sin despliegue, sin acoplamiento a Notion y sin módulos LinkML en la portada. Ver `documentacion/adr/0001-sitio-estatico-aislado.md`.
