## Descripción

<!-- Explica qué cambia este PR y por qué. Enlaza issues relacionados. -->

Fixes #<!-- issue number -->

---

## Tipo de cambio

- [ ] **feat** — Nueva funcionalidad
- [ ] **fix** — Corrección de bug
- [ ] **docs** — Solo documentación
- [ ] **style** — Formato, sin cambios de lógica
- [ ] **refactor** — Refactor sin cambio de comportamiento
- [ ] **perf** — Mejora de rendimiento
- [ ] **test** — Tests nuevos o modificados
- [ ] **chore** — Mantenimiento (deps, config, etc.)
- [ ] **ci** — Cambios en CI/CD
- [ ] **build** — Cambios en build system

---

## Checklist

### Código

- [ ] El código sigue las convenciones del proyecto (Prettier, lint)
- [ ] He añadido tests que cubren mi cambio (si aplica)
- [ ] Todos los tests pasan localmente (`make test`)
- [ ] Lint pasa (`make lint`)

### Documentación

- [ ] He actualizado la documentación afectada (README, CHANGELOG, docs/)
- [ ] He actualizado `CHANGELOG.md` en sección `[Unreleased]`
- [ ] Los comentarios en código explican el "porqué", no el "qué"

### Calidad

- [ ] No hay código comentado ni `console.log`/`print` de debug
- [ ] No hay secrets, tokens o credenciales en el diff
- [ ] El PR es atómico: un cambio lógico = un PR

### Breaking Changes

- [ ] **NO** hay breaking changes
- [ ] **SÍ** hay breaking changes (describe abajo)

---

## Breaking Changes (si aplica)

<!-- Describe qué rompe y cómo migrar -->

---

## Testing

<!-- ¿Cómo se ha probado? Incluye comandos y resultados esperados -->

```bash
# Ejemplo
make validate
```

---

## Capturas / Evidencia (si aplica)

<!-- Screenshots, logs, output de comandos -->

---

## Notas adicionales

<!-- Contexto extra, decisiones de diseño, alternativas consideradas -->
