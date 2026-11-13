#!/usr/bin/env python3
"""Local checks T01–T09 for the experimental static preview. No network required."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
HTML = ROOT / "index.html"
ALLOW = ROOT / "contenido" / "lista-permitida.md"
TOKENS = ROOT / "css" / "tokens.css"
CSS = ROOT / "css" / "sitio.css"
JS = ROOT / "js" / "menu.js"
ADR = REPO / "documentacion" / "adr" / "0001-sitio-estatico-aislado.md"
EVIDENCE_DIR = Path(__file__).resolve().parent / "evidencia"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(test_id: str, status: str, detail: str, reqs: list[str]) -> dict:
    return {
        "id": test_id,
        "status": status,
        "requirements": reqs,
        "detail": detail,
    }


def check_t01(html: str, allow: str) -> dict:
    needed = [
        "Diagnosis y Actualización del Español-Castellano",
        "Las palabras, sus fuentes y lo que significan",
        "Estado experimental",
        "no es una plataforma operativa",
        "canon aprobado",
        "Fuente",
        "Formulación",
        "Procedencia",
        "Análisis",
        "Revisión",
        "diseño y las pruebas experimentales",
        "En preparación",
    ]
    missing = [t for t in needed if t not in html]
    castigo_present = bool(re.search(r"\bCASTIGO\b", html, re.IGNORECASE))
    allow_omits_castigo = "C-07" in allow and "omitido" in allow
    private_leaks = []
    for needle in ("notion.so", "app.notion.com", ".zip", "linkml validate", "api_key", "secret"):
        if needle.lower() in html.lower():
            private_leaks.append(needle)
    if missing or castigo_present or private_leaks or not allow_omits_castigo:
        return result(
            "T01",
            "fail",
            f"missing={missing}; castigo={castigo_present}; leaks={private_leaks}; allow_castigo_ok={allow_omits_castigo}",
            ["REQ-01", "REQ-02", "REQ-03", "REQ-05", "REQ-06"],
        )
    return result(
        "T01",
        "pass",
        "Textos de lista permitida presentes; CASTIGO omitido; sin indicios de material privado en HTML.",
        ["REQ-01", "REQ-02", "REQ-03", "REQ-05", "REQ-06"],
    )


def check_t02(html: str) -> dict:
    anchors = ["#proyecto", "#metodo", "#documentacion", "#estado", "#inicio", "#contenido"]
    missing_ids = []
    for a in anchors:
        aid = a.lstrip("#")
        if f'id="{aid}"' not in html and f"id='{aid}'" not in html:
            # href targets: inicio/contenido/proyecto etc.
            if f'id="{aid}"' not in html:
                missing_ids.append(aid)
    # Ensure nav hrefs resolve to ids
    for href in ("proyecto", "metodo", "documentacion", "estado"):
        if f'id="{href}"' not in html:
            missing_ids.append(href)
    external = re.findall(r"""(?:href|src)=["']https?://[^"']+["']""", html, re.I)
    # Cards must not contain links inside documentation section — heuristic: badge En preparación near cards
    card_block = html.split('id="documentacion"', 1)[-1].split('id="estado"', 1)[0]
    card_links = re.findall(r"<a\b", card_block, re.I)
    issues = []
    if missing_ids:
        issues.append(f"missing_ids={sorted(set(missing_ids))}")
    if external:
        issues.append(f"external={external}")
    if card_links:
        issues.append(f"doc_card_links={len(card_links)}")
    if issues:
        return result("T02", "fail", "; ".join(issues), ["REQ-04", "REQ-11"])
    return result(
        "T02",
        "pass",
        "Anclas del menú existen; documentación sin enlaces; sin URLs http(s) externas. Viewports 320–1440: ensayo manual en navegador.",
        ["REQ-04", "REQ-11"],
    )


def check_t03(html: str, js: str) -> dict:
    checks = {
        "skip_link": 'href="#contenido"' in html and "Saltar al contenido" in html,
        "nav_toggle": 'id="nav-toggle"' in html and "aria-expanded" in html and "aria-controls" in html,
        "escape": "Escape" in js,
        "lang": 'lang="es"' in html,
        "h1": html.count("<h1") == 1,
        "main": "<main" in html,
    }
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        return result("T03", "fail", f"estructura incompleta: {failed}", ["REQ-07", "REQ-11"])
    return result(
        "T03",
        "pass",
        "Estructura semántica y menú con Escape presentes. Zoom 200%, reflow 400% y lector de pantalla: completar ensayo manual en evidencia de navegador.",
        ["REQ-07", "REQ-11"],
    )


def check_t04() -> dict:
    return result(
        "T04",
        "not_run",
        "Sin analizador automático instalado en este entorno de prueba (axe/pa11y/lighthouse no invocados).",
        ["REQ-07"],
    )


def check_t05(html: str, css: str, js: str) -> dict:
    remote = []
    for label, text in (("html", html), ("css", css), ("js", js)):
        for m in re.finditer(r"https?://[^\s\"')]+", text, re.I):
            remote.append(f"{label}:{m.group(0)}")
    storage = []
    for needle in ("localStorage", "sessionStorage", "document.cookie", "gtag(", "analytics"):
        if needle in html or needle in js:
            storage.append(needle)
    if remote or storage:
        return result("T05", "fail", f"remote={remote}; storage={storage}", ["REQ-08", "REQ-09"])
    return result(
        "T05",
        "pass",
        "Sin recursos remotos ni APIs de almacenamiento/cookies en el artefacto.",
        ["REQ-08", "REQ-09"],
    )


def check_t06(html: str) -> dict:
    secretish = re.findall(
        r"(?i)(api[_-]?key|secret|password|token\s*=\s*['\"][^'\"]+)",
        html,
    )
    if secretish:
        return result("T06", "fail", f"posibles secretos: {secretish}", ["REQ-05", "REQ-10"])
    return result(
        "T06",
        "pass",
        "Sin secretos obvios ni scripts externos. HTTPS/CSP de producción: not_applicable en vista previa local.",
        ["REQ-05", "REQ-10"],
    )


def check_t07() -> dict:
    return result(
        "T07",
        "sin_datos",
        "REQ-12 P1: sin medición de campo ni ensayo de laboratorio solicitado en esta fase.",
        ["REQ-12"],
    )


def check_t08() -> dict:
    with tempfile.TemporaryDirectory(prefix="sitio-rollback-") as tmp:
        tmp_path = Path(tmp)
        backup = tmp_path / "backup"
        shutil.copytree(ROOT, backup, ignore=shutil.ignore_patterns("pruebas/evidencia"))
        marker = ROOT / "index.html"
        original = marker.read_text(encoding="utf-8")
        digest_before = sha256(marker)
        try:
            marker.write_text(original + "\n<!-- rollback-probe -->\n", encoding="utf-8")
            digest_changed = sha256(marker)
            shutil.copy2(backup / "index.html", marker)
            digest_after = sha256(marker)
        finally:
            if marker.read_text(encoding="utf-8") != original:
                marker.write_text(original, encoding="utf-8")
        ok = digest_before == digest_after and digest_changed != digest_before
        if not ok:
            return result("T08", "fail", "rollback local no restauró el artefacto", ["REQ-13"])
        return result(
            "T08",
            "pass",
            f"Rollback local OK. sha256_antes={digest_before}",
            ["REQ-13"],
        )


def check_t09(tokens: str) -> dict:
    needed_files = [HTML, ALLOW, TOKENS, CSS, JS, ADR]
    missing = [str(p.relative_to(REPO)) for p in needed_files if not p.is_file()]
    focus_ok = "--focus-gap" in tokens and "--focus-ring" in tokens and "--color-focus" in tokens
    if missing or not focus_ok:
        return result(
            "T09",
            "fail",
            f"missing={missing}; focus_tokens={focus_ok}",
            ["REQ-14"],
        )
    return result(
        "T09",
        "pass",
        "ADR, lista permitida, tokens (incl. separación de foco) y componentes mínimos presentes.",
        ["REQ-14"],
    )


def main() -> int:
    html = HTML.read_text(encoding="utf-8")
    allow = ALLOW.read_text(encoding="utf-8")
    tokens = TOKENS.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")

    results = [
        check_t01(html, allow),
        check_t02(html),
        check_t03(html, js),
        check_t04(),
        check_t05(html, css, js),
        check_t06(html),
        check_t07(),
        check_t08(),
        check_t09(tokens),
    ]

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "run_id": f"sitio-local-{stamp}",
        "phase": "VALIDATE",
        "target": "sitio/",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact_sha256": {
            "index.html": sha256(HTML),
            "tokens.css": sha256(TOKENS),
            "sitio.css": sha256(CSS),
            "menu.js": sha256(JS),
            "lista-permitida.md": sha256(ALLOW),
        },
        "results": results,
    }
    out = EVIDENCE_DIR / f"run-{stamp}.json"
    latest = EVIDENCE_DIR / "latest.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")

    blocking = [r for r in results if r["status"] == "fail"]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
