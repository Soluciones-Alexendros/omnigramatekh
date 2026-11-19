#!/usr/bin/env node
/**
 * T03b + T04b — gates en navegador real (Chromium vía Playwright).
 *
 * - T04b: axe-core con las reglas de contraste ACTIVAS (jsdom no puede medirlas).
 * - T03b: reflow WCAG 1.4.10 — a 320 px CSS de ancho no debe haber scroll
 *   horizontal (equivale al 400 % de zoom sobre una ventana de 1280 px).
 *
 *   node sitio/pruebas/browser/a11y_browser.mjs
 *
 * La evidencia completa (incluido el detalle de cada violación) se escribe en
 * `sitio/pruebas/evidencia/`. Por consola solo se emite el estado por prueba:
 * el detalle nunca se vuelca a stdout/stderr.
 *
 * Exit: 0 si ambos gates pasan, 1 si alguno falla.
 */

import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createServer } from "node:net";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { AxeBuilder } from "@axe-core/playwright";
import { chromium } from "playwright";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..", "..");
// Permite apuntar a una copia temporal (tests negativos sin mutar el repo).
const SITE_DIR = process.env.SITIO_DIR
  ? path.resolve(process.env.SITIO_DIR)
  : path.join(REPO, "sitio");
const EVIDENCE_DIR = path.join(REPO, "sitio", "pruebas", "evidencia");

const WCAG_TAGS = [
  "wcag2a",
  "wcag2aa",
  "wcag21a",
  "wcag21aa",
  "wcag22aa",
  "best-practice",
];
// Umbral de tolerancia de subpíxel para el reflow (por redondeo del layout).
const REFLOW_TOLERANCE_PX = 1;

function freePort() {
  return new Promise((resolve, reject) => {
    const srv = createServer();
    srv.once("error", reject);
    srv.listen(0, "127.0.0.1", () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

async function waitForServer(url, timeoutMs = 10_000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch {
      // servidor aún arrancando
    }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error(`servidor local no respondió en ${timeoutMs} ms: ${url}`);
}

function startStaticServer(port) {
  const child = spawn(
    "python3",
    [
      "-m",
      "http.server",
      String(port),
      "--bind",
      "127.0.0.1",
      "--directory",
      SITE_DIR,
    ],
    { stdio: ["ignore", "ignore", "pipe"] }
  );
  return child;
}

async function sha256File(file) {
  return createHash("sha256")
    .update(await readFile(file))
    .digest("hex");
}

function summarizeViolations(violations) {
  return violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    help: v.help,
    nodes: v.nodes.length,
    // Solo selectores: nunca el HTML del nodo (podría arrastrar contenido).
    targets: v.nodes.slice(0, 5).map((n) => n.target),
  }));
}

async function main() {
  const port = await freePort();
  const base = `http://127.0.0.1:${port}/`;
  const server = startStaticServer(port);

  const results = [];
  let exitCode = 0;

  try {
    await waitForServer(`${base}index.html`);

    const browser = await chromium.launch();
    try {
      // --- T04b: accesibilidad con contraste real ---
      const desktop = await browser.newContext({
        viewport: { width: 1280, height: 800 },
      });
      const page = await desktop.newPage();
      await page.goto(`${base}index.html`, { waitUntil: "load" });

      const axeResults = await new AxeBuilder({ page })
        .withTags(WCAG_TAGS)
        // Aquí SÍ se miden: Chromium tiene canvas y motor de estilos.
        .analyze();

      results.push({
        id: "T04b",
        status: axeResults.violations.length === 0 ? "pass" : "fail",
        detail: {
          violations: summarizeViolations(axeResults.violations),
          incomplete: axeResults.incomplete.map((r) => r.id),
          passes: axeResults.passes.length,
        },
      });
      if (axeResults.violations.length > 0) exitCode = 1;

      // --- T03b: reflow 320 px (WCAG 1.4.10) ---
      await page.setViewportSize({ width: 320, height: 800 });
      await page.reload({ waitUntil: "load" });
      const overflow = await page.evaluate(() => {
        const el = document.documentElement;
        return {
          scrollWidth: el.scrollWidth,
          clientWidth: el.clientWidth,
          // Elementos que sobresalen del viewport (solo para diagnóstico).
          widest: [...document.querySelectorAll("body *")]
            .map((n) => {
              const r = n.getBoundingClientRect();
              return {
                tag: n.tagName.toLowerCase(),
                right: Math.round(r.right),
              };
            })
            .filter((n) => n.right > el.clientWidth + 1)
            .slice(0, 5),
        };
      });

      const reflowOk =
        overflow.scrollWidth <= overflow.clientWidth + REFLOW_TOLERANCE_PX;
      results.push({
        id: "T03b",
        status: reflowOk ? "pass" : "fail",
        detail: overflow,
      });
      if (!reflowOk) exitCode = 1;

      await desktop.close();
    } finally {
      await browser.close();
    }
  } finally {
    server.kill("SIGTERM");
  }

  const stamp = new Date()
    .toISOString()
    .replace(/[-:]/g, "")
    .replace(/\..+/, "Z");
  const payload = {
    run_id: `sitio-browser-${stamp}`,
    phase: "VALIDATE",
    target: "sitio/ (chromium)",
    generated_at: new Date().toISOString(),
    artifact_sha256: {
      "index.html": await sha256File(path.join(SITE_DIR, "index.html")),
    },
    gate: {
      status: exitCode === 0 ? "pass" : "fail",
      blocking: results.filter((r) => r.status === "fail").map((r) => r.id),
    },
    results,
  };

  await mkdir(EVIDENCE_DIR, { recursive: true });
  const out = path.join(EVIDENCE_DIR, `browser-${stamp}.json`);
  await writeFile(out, JSON.stringify(payload, null, 2) + "\n", "utf-8");

  console.log(
    `sitio/pruebas/browser: evidencia escrita en ${path.relative(REPO, out)}`
  );
  for (const r of results) console.log(`  ${r.id}: ${r.status}`);
  console.error(
    `\ngate: ${payload.gate.status} (${results.length} comprobaciones en navegador)`
  );

  return exitCode;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error(`error en gates de navegador: ${err.message}`);
    process.exit(1);
  }
);
