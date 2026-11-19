# Spec: MEJORA-01 — Gates en navegador real

> Origen: auditoría crítica, MEJORA-01 («cerrar en navegador real lo que hoy es
> "manual" o "sin datos"»). Estado: en ejecución.

## Objective

Que T03 (zoom/reflow), T04 (contraste) y T07 (REQ-12, rendimiento) dejen de ser
pendientes y pasen a ser comprobaciones automáticas ejecutables en local y en CI:

- **T04b** — accesibilidad con `@axe-core/playwright` en Chromium real, con reglas
  de **contraste de color activas** (jsdom no puede medirlas: sin canvas).
- **T03b** — reflow: a 320 px CSS de ancho no debe haber scroll horizontal
  (WCAG 1.4.10 Reflow, equivalente al 400 % de zoom en 1280 px).
- **T07** — presupuesto de rendimiento medible con Lighthouse CI sobre el sitio
  servido en local (categorías performance/accessibility y métricas CWV).

## Tech Stack

- Node 24, ESM (`.mjs`), `node:test` para orquestar.
- `playwright` + `@axe-core/playwright` (Chromium headless).
- `@lhci/cli` (Lighthouse CI, `collect` + `assert`).
- Servidor local efímero: `python3 -m http.server` ya disponible (sin dependencia
  nueva), servido sobre `sitio/`.

## Commands

```bash
# Gates de navegador (descarga Chromium la primera vez)
npm run test:browser
# A11y + reflow (Playwright + axe)
npm run test:browser:a11y
# Rendimiento (Lighthouse CI con presupuestos)
npm run test:browser:perf
```

## Project Structure

```
sitio/pruebas/
├── browser/
│   ├── a11y_browser.mjs      # axe-core real + reflow 320px
│   └── lighthouserc.json     # presupuestos CWV (assert)
├── evidencia/                # evidencia curada (JSON con sha256)
└── test_a11y.js              # se conserva: fallback rápido sin navegador
```

## Code Style

- ESM, `node:test`, sin dependencias fuera de devDependencies existentes.
- Salida legible en CI; el detalle completo se escribe en JSON, no en stdout
  (regla aprendida del hallazgo CodeQL de la fase anterior).

## Testing Strategy

- **Negativo obligatorio**: inyectar un fallo real (contraste insuficiente,
  overflow horizontal y meta viewport ausente) y comprobar que cada gate falla.
- **Positivo**: el sitio actual debe pasar los tres.
- **CI**: job dedicado `browser-gates` para no penalizar el tiempo de los tests
  unitarios; Chromium cacheado.

## Boundaries

- Always: umbrales declarados y justificados; fallo explícito con exit ≠ 0.
- Ask first: cambiar presupuestos de rendimiento; añadir servicios externos.
- Never: sustituir el gate de jsdom sin mantener el fallback; subir el presupuesto
  para «hacer pasar» un test.

## Success Criteria

1. `npm run test:browser:a11y` falla si hay violación de contraste en Chromium.
2. `npm run test:browser` detecta overflow horizontal a 320 px.
3. `npm run test:browser:perf` aplica presupuestos y falla si no se cumplen.
4. Los tres pasan sobre `sitio/` actual.
5. CI ejecuta todo en un job propio y en verde.

## Open Questions

- ¿Fijar presupuestos CWV a valores de laboratorio (LCP < 2.5 s, CLS < 0.1,
  TBT < 200 ms) o solo las categorías? → Se fijan los de laboratorio; son
  reproducibles y ya exigen calidad real a un sitio de 100 KB.
