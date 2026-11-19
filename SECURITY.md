# Política de Seguridad

### Propósito de este documento

Define la política de seguridad del proyecto: versiones soportadas, proceso de reporte de vulnerabilidades (divulgación coordinada), alcance, y contacto. No hay versiones con soporte LTS (fase experimental 0.x).

---

## Versiones Soportadas

Actualmente este proyecto está en fase experimental (0.x). No hay versiones con soporte LTS (long-term support). **No obstante**, nos comprometemos a evaluar y parchear vulnerabilidades críticas en la rama `main` según el SLA abajo.

| Versión    | Soportada      | Nota                                |
| ---------- | -------------- | ----------------------------------- |
| 0.x (main) | ⚠️ Best-effort | Sin LTS; parches críticos en `main` |

## Reporte de Vulnerabilidades

Si descubres una vulnerabilidad de seguridad, por favor **no abras un issue público**. En su lugar:

1. Envía un correo a: **security@alexendros.dev**
2. Incluye:
   - Descripción de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial
   - Cualquier prueba de concepto (si existe)

Nos comprometemos a:

- Acusar recibo en 48 horas
- Proporcionar una evaluación inicial en 7 días
- Mantener informado al reportero del progreso

## Alcance

Esta política cubre:

- Código en este repositorio (sitio estático, herramientas LinkML, scripts)
- Dependencias declaradas en `package.json`
- Workflows de GitHub Actions (`.github/workflows/`)

Queda fuera de alcance:

- Infraestructura de GitHub (gestionada por GitHub)
- Dependencias del sistema operativo
- Herramientas de desarrollo no declaradas en el repo

## Divulgación Coordinada

Seguimos un modelo de divulgación coordinada:

1. Reporte privado → 2. Evaluación → 3. Corrección → 4. Publicación de aviso (si procede) → 5. Divulgación pública tras parche

## Contacto

- **Email**: security@alexendros.dev
- **PGP**: Disponible bajo petición
