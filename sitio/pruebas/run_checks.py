#!/usr/bin/env python3
"""Local checks T01–T09 for the experimental static preview. No network required."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, UTC
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


# Secret detection patterns - regex-based, not substring matching
# These match actual secret formats, not words like "secretaría"
SECRET_PATTERNS = [
    # AWS Access Key ID
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS Access Key ID"),
    # GitHub Personal Access Token (classic)
    (re.compile(r"\bghp_[a-zA-Z0-9]{36}\b"), "GitHub PAT (classic)"),
    # GitHub Fine-grained PAT
    (re.compile(r"\bgithub_pat_[a-zA-Z0-9_]{82}\b"), "GitHub Fine-grained PAT"),
    # GitHub OAuth token
    (re.compile(r"\bgho_[a-zA-Z0-9]{36}\b"), "GitHub OAuth token"),
    # GitHub App token
    (re.compile(r"\bghs_[a-zA-Z0-9]{36}\b"), "GitHub App token"),
    # GitHub Refresh token
    (re.compile(r"\bghr_[a-zA-Z0-9]{36}\b"), "GitHub Refresh token"),
    # Private keys (PEM)
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"), "Private Key (PEM)"),
    # Generic secret assignment patterns (key=value or key: value with quoted value >=8 chars)
    (re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\'][^"\']{8,}'), "Secret assignment"),
]


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
    for needle in ("notion.so", "app.notion.com", ".zip", "linkml validate"):
        if needle.lower() in html.lower():
            private_leaks.append(needle)
    # Secret detection via regex patterns (not substrings)
    secret_leaks = []
    for pattern, label in SECRET_PATTERNS:
        matches = pattern.findall(html)
        if matches:
            # No se registra el valor del secreto: solo tipo y número de coincidencias.
            secret_leaks.append(f"{label} ({len(matches)} coincidencia(s))")
    all_leaks = private_leaks + secret_leaks
    if missing or castigo_present or all_leaks or not allow_omits_castigo:
        return result(
            "T01",
            "fail",
            f"missing={missing}; castigo={castigo_present}; leaks={all_leaks}; allow_castigo_ok={allow_omits_castigo}",
            ["REQ-01", "REQ-02", "REQ-03", "REQ-05", "REQ-06"],
        )
    return result(
        "T01",
        "pass",
        "Textos de lista permitida presentes; CASTIGO omitido; sin indicios de material privado en HTML.",
        ["REQ-01", "REQ-02", "REQ-03", "REQ-05", "REQ-06"],
    )


def check_t02(html: str) -> dict:
    from html.parser import HTMLParser

    class AnchorCollector(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids = set()
            self.external_urls = []
            self.in_doc_section = False
            self.doc_section_links = 0

        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            # Collect all id attributes
            if "id" in attrs_dict:
                self.ids.add(attrs_dict["id"])
                # Track section boundaries
                if attrs_dict["id"] == "documentacion":
                    self.in_doc_section = True
                elif attrs_dict["id"] == "estado" and self.in_doc_section:
                    self.in_doc_section = False
            # Collect external URLs
            for attr in ("href", "src"):
                if attr in attrs_dict and attrs_dict[attr].startswith("http"):
                    self.external_urls.append(attrs_dict[attr])
            # Count links inside documentation section
            if self.in_doc_section and tag.lower() == "a":
                self.doc_section_links += 1

    parser = AnchorCollector()
    parser.feed(html)

    required_ids = {"inicio", "contenido", "proyecto", "metodo", "documentacion", "estado"}
    missing_ids = sorted(required_ids - parser.ids)

    issues = []
    if missing_ids:
        issues.append(f"missing_ids={missing_ids}")
    if parser.external_urls:
        issues.append(f"external={parser.external_urls}")
    if parser.doc_section_links:
        issues.append(f"doc_card_links={parser.doc_section_links}")
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


# T04 (accesibilidad automática) vive en sitio/pruebas/test_a11y.js: axe-core sobre
# el HTML real, ejecutado por `npm run test:js`. Aquí no se duplica ni se finge.


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
    secret_leaks = []
    for pattern, label in SECRET_PATTERNS:
        matches = pattern.findall(html)
        if matches:
            # No se registra el valor del secreto: solo tipo y número de coincidencias.
            secret_leaks.append(f"{label} ({len(matches)} coincidencia(s))")
    if secret_leaks:
        return result("T06", "fail", f"secretos detectados: {secret_leaks}", ["REQ-05", "REQ-10"])
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
        check_t05(html, css, js),
        check_t06(html),
        check_t07(),
        check_t09(tokens),
    ]

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    # El gate no promociona lo no verificado: separa lo que bloquea de lo que
    # queda pendiente de comprobación manual o de datos.
    blocking = [r for r in results if r["status"] == "fail"]
    unverified = [
        {"id": r["id"], "status": r["status"], "reason": r["detail"]}
        for r in results
        if r["status"] not in ("pass", "fail")
    ]
    gate = {
        "status": "pass" if not blocking else "fail",
        "blocking": [r["id"] for r in blocking],
        "unverified": unverified,
        "counts": {
            "pass": sum(1 for r in results if r["status"] == "pass"),
            "fail": len(blocking),
            "unverified": len(unverified),
        },
    }

    payload = {
        "run_id": f"sitio-local-{stamp}",
        "phase": "VALIDATE",
        "target": "sitio/",
        "generated_at": datetime.now(UTC).isoformat(),
        "artifact_sha256": {
            "index.html": sha256(HTML),
            "tokens.css": sha256(TOKENS),
            "sitio.css": sha256(CSS),
            "menu.js": sha256(JS),
            "lista-permitida.md": sha256(ALLOW),
        },
        "gate": gate,
        "results": results,
    }
    out = EVIDENCE_DIR / f"run-{stamp}.json"
    latest = EVIDENCE_DIR / "latest.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    counts = gate["counts"]
    print(
        f"\ngate: {gate['status']} · {counts['pass']} pass · "
        f"{counts['fail']} fail · {counts['unverified']} sin verificar",
        file=sys.stderr,
    )
    if unverified:
        detail = ", ".join(f"{u['id']}={u['status']}" for u in unverified)
        print(f"pendiente de verificación: {detail} (ver sitio/pruebas/matriz.md)", file=sys.stderr)

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
