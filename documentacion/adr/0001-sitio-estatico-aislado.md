# ADR 0001 · Sitio estático aislado

- **Estado:** aceptado para vista previa local experimental
- **Fecha:** 2026-11-13
- **Contexto:** Spec · Web pública y sistema de diseño · 2026-11-13; Informe · Contenidos para la web pública · 2026-11-13

## Decisión

La superficie pública vive solo bajo `sitio/` como HTML/CSS/JS estático (opción A de la especificación, sección 6). No usa generador estático, framework, backend, CMS ni conexión a Notion.

El árbol `sitio/` queda fuera de cualquier módulo léxico futuro (`esquema/`, `controles/`, `proyecciones/`, `ejemplos/`, `historico/`). El sitio no lee YAML LinkML, ZIP históricos ni páginas privadas.

## Consecuencias

- Contenido público solo desde `sitio/contenido/` y la lista permitida versionada.
- Vista previa local con servidor estático o apertura de archivos; sin dominio, hosting, despliegue ni publicación en esta fase.
- Sin analítica, formularios, cookies no necesarias, scripts de terceros ni embeds.
- CASTIGO omitido hasta decisión expresa del operador.
- Tarjetas de documentación en estado «En preparación» hasta que exista un destino público revisado.
- Tipografía de sistema local; tokens tomados de la sección 4 de la especificación (propuesta v0, no identidad definitiva).
- Publicación, HTTPS de producción y proveedor de alojamiento requieren ADR posteriores y autorización expresa.

## Alternativas consideradas

- **Generador estático (opción B):** aplazado; el MVP es una sola portada con anclas.
- **Mezclar la web con el árbol LinkML:** rechazado; aumenta el riesgo de exponer material experimental o privado.
