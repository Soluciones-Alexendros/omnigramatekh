# Sitio · vista previa local experimental

Portada estática de OmniGramatekh para ensayo local. No es un sitio publicado ni una plataforma operativa.

## Arranque local

Desde este directorio:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Abrir `http://127.0.0.1:8765/` en el navegador. Detener el servidor al terminar.

## Contenido

Solo piezas de `contenido/lista-permitida.md`. CASTIGO, contacto, legales y enlaces externos quedan omitidos.

## Pruebas

```bash
npm test                    # desde la raíz: checks del sitio + menú
npm run test:sitio          # solo T01–T09 (Python)
npm run test:js             # solo comportamiento de menu.js (Node)
```

La matriz REQ → prueba está en `pruebas/matriz.md`. La evidencia de la última
ejecución queda en `pruebas/evidencia/latest.json` (estado local, no versionado);
solo se versionan las corridas curadas.

## Límites

- Sin despliegue, analítica, formularios ni scripts de terceros.
- Sin acoplamiento a módulos LinkML ni a Notion.
- Tokens visuales: propuesta v0 (Spec §4), no identidad definitiva.
