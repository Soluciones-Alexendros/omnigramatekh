# Matriz REQ → prueba · sitio experimental

Estado: vista previa local. Ninguna prueba certifica conformidad legal ni WCAG completa.

Gates automáticos (`npm test`) y de navegador real (`npm run test:browser`:
Chromium, contraste efectivo, reflow y presupuestos de rendimiento). T08 se
retiró por tautológico (comprobaba `shutil.copy2`, no un mecanismo del proyecto).

| Prueba                         | Requisitos       | Procedimiento local                                                                                                                              | Evidencia                                          |
| ------------------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| T01 · Veracidad y contenido    | REQ-01–03, 05–06 | Comparar `index.html` con `contenido/lista-permitida.md`; confirmar estado experimental, cinco etapas, ausencia de CASTIGO y de material privado | `run_checks.py` · T01                              |
| T02 · Rutas y estados          | REQ-04, 11       | Anclas del menú existen; tarjetas sin `<a>`; sin `http(s):` externos; comprobar viewports en navegador                                           | `run_checks.py` · T02 + ensayo manual              |
| T03 · Accesibilidad manual     | REQ-07, 11       | Teclado, Escape en menú, foco visible, skip link; reflow a 320 px (WCAG 1.4.10) en Chromium                                                      | `test_menu.js` + `browser/a11y_browser.mjs` · T03b |
| T04 · Accesibilidad automática | REQ-07           | axe-core WCAG 2.1/2.2 AA en jsdom **y** en Chromium con contraste real activo                                                                    | `test_a11y.js` + `browser/a11y_browser.mjs` · T04b |
| T05 · Red y datos              | REQ-08–09        | HTML sin scripts/estilos remotos; sin cookies ni storage en código                                                                               | `run_checks.py` · T05                              |
| T06 · Seguridad del artefacto  | REQ-05, 10       | Sin secretos obvios; sin HTML de usuario; sin scripts externos; HTTPS de producción `not_applicable` en local                                    | `run_checks.py` · T06                              |
| T07 · Rendimiento              | REQ-12           | Presupuestos de laboratorio con Lighthouse CI: perf ≥ 0.9, LCP ≤ 2.5 s, CLS ≤ 0.1, TBT ≤ 200 ms                                                  | `browser/lighthouserc.json` · `test:browser:perf`  |
| T09 · Handoff                  | REQ-14           | Tokens, componentes y ADR presentes; contraste foco/acción documentado                                                                           | `run_checks.py` · T09                              |
