(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");

  if (!toggle || !nav) {
    return;
  }

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      nav.removeAttribute("hidden");
    } else {
      nav.setAttribute("hidden", "");
    }
  }

  function isDesktop() {
    return window.matchMedia("(min-width: 48rem)").matches;
  }

  function syncForViewport() {
    if (isDesktop()) {
      nav.removeAttribute("hidden");
      toggle.setAttribute("aria-expanded", "false");
    } else if (toggle.getAttribute("aria-expanded") !== "true") {
      nav.setAttribute("hidden", "");
    }
  }

  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") !== "true";
    setOpen(open);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
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

  window.addEventListener("resize", syncForViewport);
  syncForViewport();
})();
