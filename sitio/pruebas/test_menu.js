#!/usr/bin/env node
/**
 * Pruebas de comportamiento del menú de navegación (sitio/js/menu.js).
 * Sin navegador: un DOM mínimo en memoria. Sin red, sin dependencias.
 *
 *   node --test sitio/pruebas/test_menu.js
 */

"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { initMenu } = require("../js/menu.js");

/** Elemento mínimo con atributos, listeners y foco. */
class FakeElement {
  constructor(id) {
    this.id = id;
    this.attributes = new Map();
    this.listeners = new Map();
    this.focused = false;
    this.children = [];
  }

  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  getAttribute(name) {
    return this.attributes.has(name) ? this.attributes.get(name) : null;
  }

  removeAttribute(name) {
    this.attributes.delete(name);
  }

  hasAttribute(name) {
    return this.attributes.has(name);
  }

  addEventListener(type, handler) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, []);
    }
    this.listeners.get(type).push(handler);
  }

  dispatch(type, event) {
    for (const handler of this.listeners.get(type) || []) {
      handler(event || {});
    }
  }

  focus() {
    this.focused = true;
  }

  querySelectorAll(selector) {
    return selector === "a" ? this.children : [];
  }
}

function makeDocument(elements) {
  const doc = new FakeElement("#document");
  doc.getElementById = (id) => elements.get(id) || null;
  return doc;
}

function makeWindow(desktop) {
  const win = new FakeElement("#window");
  win.matchMedia = () => ({ matches: desktop });
  return win;
}

function setup({ desktop = false, withNav = true, links = 0 } = {}) {
  const toggle = new FakeElement("nav-toggle");
  toggle.setAttribute("aria-expanded", "false");
  const nav = new FakeElement("site-nav");
  nav.setAttribute("hidden", "");
  for (let i = 0; i < links; i += 1) {
    nav.children.push(new FakeElement(`a${i}`));
  }
  const elements = new Map();
  if (withNav) {
    elements.set("nav-toggle", toggle);
    elements.set("site-nav", nav);
  }
  const doc = makeDocument(elements);
  const win = makeWindow(desktop);
  const menu = initMenu(doc, win);
  return { menu, doc, win, toggle, nav };
}

test("sin nodos en el documento no falla y no devuelve controlador", () => {
  const { menu } = setup({ withNav: false });
  assert.equal(menu, null);
});

test("el clic abre y cierra el menú en móvil", () => {
  const { toggle, nav } = setup({ desktop: false });

  assert.ok(nav.hasAttribute("hidden"), "arranca plegado en móvil");

  toggle.dispatch("click");
  assert.equal(toggle.getAttribute("aria-expanded"), "true");
  assert.equal(nav.hasAttribute("hidden"), false);

  toggle.dispatch("click");
  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.ok(nav.hasAttribute("hidden"));
});

test("Escape cierra el menú y devuelve el foco al botón", () => {
  const { doc, toggle, nav } = setup({ desktop: false });

  toggle.dispatch("click");
  assert.equal(toggle.getAttribute("aria-expanded"), "true");

  doc.dispatch("keydown", { key: "Escape" });

  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.ok(nav.hasAttribute("hidden"));
  assert.ok(toggle.focused, "el foco vuelve al botón");
});

test("Escape con el menú cerrado no hace nada", () => {
  const { doc, toggle } = setup({ desktop: false });
  toggle.focused = false;

  doc.dispatch("keydown", { key: "Escape" });

  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.equal(toggle.focused, false);
});

test("en escritorio el menú queda visible y aria-expanded en false", () => {
  const { toggle, nav } = setup({ desktop: true });

  assert.equal(nav.hasAttribute("hidden"), false);
  assert.equal(toggle.getAttribute("aria-expanded"), "false");
});

test("un enlace del menú cierra el panel en móvil", () => {
  const { toggle, nav } = setup({ desktop: false, links: 1 });
  const link = nav.children[0];

  toggle.dispatch("click");
  assert.equal(toggle.getAttribute("aria-expanded"), "true");

  link.dispatch("click");

  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.ok(nav.hasAttribute("hidden"));
});

test("un enlace del menú no cierra nada en escritorio", () => {
  const { toggle, nav } = setup({ desktop: true, links: 1 });
  const link = nav.children[0];

  link.dispatch("click");

  assert.equal(toggle.getAttribute("aria-expanded"), "false");
  assert.equal(nav.hasAttribute("hidden"), false);
});

test("al redimensionar a escritorio se despliega; a móvil se repliega", () => {
  let desktop = false;
  const toggle = new FakeElement("nav-toggle");
  toggle.setAttribute("aria-expanded", "false");
  const nav = new FakeElement("site-nav");
  nav.setAttribute("hidden", "");
  const doc = makeDocument(
    new Map([
      ["nav-toggle", toggle],
      ["site-nav", nav],
    ])
  );
  const win = new FakeElement("#window");
  win.matchMedia = () => ({ matches: desktop });
  initMenu(doc, win);

  assert.ok(nav.hasAttribute("hidden"), "móvil: plegado");

  desktop = true;
  win.dispatch("resize");
  assert.equal(nav.hasAttribute("hidden"), false, "escritorio: visible");

  desktop = false;
  win.dispatch("resize");
  assert.ok(nav.hasAttribute("hidden"), "vuelve a móvil: plegado");
});
