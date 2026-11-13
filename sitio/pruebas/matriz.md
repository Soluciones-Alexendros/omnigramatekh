# Matriz REQ → prueba · sitio experimental

Estado: vista previa local. Ninguna prueba certifica conformidad legal ni WCAG completa.

| Prueba | Requisitos | Procedimiento local | Evidencia |
| --- | --- | --- | --- |
| T01 · Veracidad y contenido | REQ-01–03, 05–06 | Comparar `index.html` con `contenido/lista-permitida.md`; confirmar estado experimental, cinco etapas, ausencia de CASTIGO y de material privado | `run_checks.py` · T01 |
| T02 · Rutas y estados | REQ-04, 11 | Anclas del menú existen; tarjetas sin `<a>`; sin `http(s):` externos; comprobar viewports en navegador | `run_checks.py` · T02 + ensayo manual |
| T03 · Accesibilidad manual | REQ-07, 11 | Teclado, Escape en menú, foco visible, skip link; zoom/reflow en navegador | ensayo en navegador · notas en evidencia |
| T04 · Accesibilidad automática | REQ-07 | Analizador si está disponible; si no, `not_run` con motivo | `run_checks.py` · T04 |
| T05 · Red y datos | REQ-08–09 | HTML sin scripts/estilos remotos; sin cookies ni storage en código | `run_checks.py` · T05 |
| T06 · Seguridad del artefacto | REQ-05, 10 | Sin secretos obvios; sin HTML de usuario; sin scripts externos; HTTPS de producción `not_applicable` en local | `run_checks.py` · T06 |
| T07 · Rendimiento | REQ-12 | Sin medición de campo aprobada → `sin datos` | `run_checks.py` · T07 |
| T08 · Recuperación | REQ-13 | Copia del artefacto, sustitución y restauración local | `run_checks.py` · T08 |
| T09 · Handoff | REQ-14 | Tokens, componentes y ADR presentes; contraste foco/acción documentado | `run_checks.py` · T09 |
