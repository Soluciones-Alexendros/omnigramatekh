#!/usr/bin/env node
/**
 * Prueba de accesibilidad automática (T04) con axe-core sobre el HTML real.
 *
 * Sin navegador: JSDOM parsea `sitio/index.html` y axe-core lo analiza.
 * Se pasa `document.documentElement` como contexto porque axe deduce `window`
 * y `document` del `ownerDocument` del elemento (sus variables internas no son
 * globales).
 *
 *   node --test sitio/pruebas/test_a11y.js
 *
 * Si axe-core o jsdom no están instalados (MODULE_NOT_FOUND), la prueba se omite
 * en local, pero **falla en CI** (process.env.CI) para que un gate roto no pase
 * inadvertido.
 */

"use strict";

const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const HTML_FILE = path.resolve(__dirname, "..", "index.html");

const STANDARD_TAGS = [
  "wcag2a",
  "wcag2aa",
  "wcag21a",
  "wcag21aa",
  "best-practice",
];

function loadTooling() {
  try {
    const axe = require("axe-core");
    const { JSDOM } = require("jsdom");
    return { axe, JSDOM };
  } catch (err) {
    // Solo MODULE_NOT_FOUND es legítimo para "omitir"; cualquier otro error
    // (versión incompatible, error de sintaxis, módulo roto) debe fallar.
    if (err.code === "MODULE_NOT_FOUND") {
      return null;
    }
    throw err;
  }
}

function summarize(violations) {
  return violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    nodes: v.nodes.length,
    description: v.description,
    helpUrl: v.helpUrl,
  }));
}

test("T04 · accesibilidad automática (axe-core, WCAG 2.1 AA)", async (t) => {
  const tooling = loadTooling();
  const inCI = Boolean(process.env.CI);

  if (!tooling) {
    const msg =
      "axe-core o jsdom no instalados (MODULE_NOT_FOUND): T04 omitido";
    if (inCI) {
      // En CI, un gate roto no puede pasar como "skip"
      throw new Error(`${msg} — fallando en CI para evitar falso verde`);
    }
    t.skip(msg);
    return;
  }

  const { axe, JSDOM } = tooling;
  const dom = new JSDOM(fs.readFileSync(HTML_FILE, "utf-8"), {
    url: "http://localhost/",
    pretendToBeVisual: true,
  });

  const results = await axe.run(dom.window.document.documentElement, {
    runOnly: { type: "tag", values: STANDARD_TAGS },
    rules: {
      // jsdom no implementa canvas: axe no puede medir contraste de color.
      // Queda como revisión manual, no como aprobado.
      "color-contrast": { enabled: false },
      "color-contrast-enhanced": { enabled: false },
    },
  });

  if (results.violations.length > 0) {
    throw new Error(
      `${results.violations.length} violación(es) de accesibilidad:\n` +
        JSON.stringify(summarize(results.violations), null, 2)
    );
  }

  console.log(
    `axe-core: ${results.passes.length} reglas pasan, ` +
      `${results.incomplete.length} requieren revisión manual, ` +
      `${results.violations.length} violaciones. ` +
      "Contraste de color: excluido (jsdom sin canvas), se verifica a mano."
  );
});
