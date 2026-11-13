# Ensayo de navegador · 2026-11-13

Entorno: `python3 -m http.server 8765 --bind 127.0.0.1` en `sitio/`.  
URL: `http://127.0.0.1:8765/`. Sin publicación.

## Comportamiento verificado

| Acción | Resultado |
| --- | --- |
| Carga inicial (desktop) | H1, aviso experimental, cinco etapas y tarjetas «En preparación» visibles |
| Navegación `#metodo` | URL pasa a `/#metodo`; sección Método en el documento |
| Viewport 375 × 812 | Botón «Menú» con `aria-expanded` / estado collapsed |
| Abrir menú | Estado expanded; enlaces Proyecto/Método/Documentación/Estado disponibles |
| Escape | Menú collapsed; foco permanece en el botón Menú |
| CTA «Conocer el proyecto» | URL `/#proyecto` |
| Overflow horizontal a 375 px | `scrollWidth === clientWidth === 375` |
| Cookies / localStorage | cookie vacía; `storageKeys: []` |

## Pendiente / no ejecutado

- Zoom 200 % y reflow 400 % sistemáticos en todos los viewports listados (320, 768, 1024, 1440).
- Lector de pantalla.
- T04 (axe/pa11y/lighthouse): `not_run`.
- T07 campo/laboratorio: `sin_datos`.
