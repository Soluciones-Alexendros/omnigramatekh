/**
 * Menú de navegación del sitio: plegado en móvil, siempre visible en escritorio.
 *
 * Se escribe como factoría para poder probarla en Node sin navegador: `initMenu`
 * recibe el documento y la ventana, no los toma de globales.
 */
(function (global, factory) {
  var api = factory();

  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }

  if (global && global.document) {
    global.OmniMenu = api;
    api.initMenu(global.document, global);
  }
})(typeof window !== "undefined" ? window : globalThis, function () {
  var DESKTOP_QUERY = "(min-width: 48rem)";

  function initMenu(doc, win) {
    var toggle = doc.getElementById("nav-toggle");
    var nav = doc.getElementById("site-nav");

    if (!toggle || !nav) {
      return null;
    }

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        nav.removeAttribute("hidden");
      } else {
        nav.setAttribute("hidden", "");
      }
    }

    function isOpen() {
      return toggle.getAttribute("aria-expanded") === "true";
    }

    function isDesktop() {
      return win.matchMedia(DESKTOP_QUERY).matches;
    }

    function syncForViewport() {
      if (isDesktop()) {
        nav.removeAttribute("hidden");
        toggle.setAttribute("aria-expanded", "false");
      } else if (!isOpen()) {
        nav.setAttribute("hidden", "");
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (!isDesktop()) {
          setOpen(false);
        }
      });
    });

    win.addEventListener("resize", syncForViewport);
    syncForViewport();

    return {
      setOpen: setOpen,
      isOpen: isOpen,
      syncForViewport: syncForViewport,
    };
  }

  return { initMenu: initMenu, DESKTOP_QUERY: DESKTOP_QUERY };
});
