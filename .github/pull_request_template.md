# Pull Request — Always Beautiful Operations Platform

## 1. Resumen

Este Pull Request integra un bloque específico del proyecto Always Beautiful Operations Platform.

Describe brevemente qué se implementa, corrige, documenta o prepara en este PR.

---

## 2. Alcance incluido

- 

---

## 3. Alcance excluido

Indicar explícitamente qué NO forma parte de este PR.

- 

---

## 4. Módulo afectado

Marca el módulo principal afectado:

- [ ] Foundation Layer
- [ ] Observability + Security
- [ ] Orders Core
- [ ] Payments Core
- [ ] Shipping Core
- [ ] Notifications
- [ ] Booking Engine
- [ ] Schedule Engine
- [ ] Catalog
- [ ] Cart + Checkout
- [ ] Admin Panel Backend
- [ ] Admin Panel Frontend
- [ ] Storefront Experience
- [ ] Recommendation + Assistant Intelligence Layer
- [ ] Documentation
- [ ] DevOps / Tooling
- [ ] Integrations
- [ ] Marketing / Canva

---

## 5. Tipo de cambio

- [ ] `feat` — Nueva funcionalidad
- [ ] `fix` — Corrección
- [ ] `style` — Ajuste visual o de formato sin cambiar lógica central
- [ ] `refactor` — Reorganización interna sin cambiar comportamiento externo
- [ ] `docs` — Documentación
- [ ] `test` — Pruebas
- [ ] `build` — Dependencias, tooling o build system
- [ ] `chore` — Mantenimiento general

---

## 6. Validaciones ejecutadas

### Frontend

- [ ] `npm --prefix web run build`
- [ ] Revisión visual desktop
- [ ] Revisión visual tablet
- [ ] Revisión visual móvil
- [ ] Confirmación de que `/admin` no se rompe si aplica Storefront

### Backend

- [ ] `pytest`
- [ ] Validación manual de endpoints si aplica
- [ ] Validación de Swagger si aplica
- [ ] Validación de rutas protegidas si aplica

### Git

- [ ] `git status --short`
- [ ] `git log --oneline --graph --decorate -10`

---

## 7. Riesgos revisados

Indicar riesgos técnicos, visuales, de arquitectura, seguridad, datos, dependencias o integración.

- 

---

## 8. Decisiones técnicas

Explicar decisiones relevantes tomadas durante el desarrollo.

- 

---

## 9. Datos reales o mocks

Indicar si este PR usa datos reales, mocks o placeholders.

- [ ] Usa datos reales
- [ ] Usa datos mock
- [ ] Usa placeholders formales
- [ ] No aplica

Detalle:

- 

---

## 10. Impacto sobre módulos existentes

Indicar si este PR puede afectar otros módulos.

- [ ] No afecta otros módulos
- [ ] Puede afectar Storefront
- [ ] Puede afectar Admin Dashboard
- [ ] Puede afectar Backend
- [ ] Puede afectar rutas
- [ ] Puede afectar estilos globales
- [ ] Puede afectar dependencias
- [ ] Puede afectar documentación

Detalle:

- 

---

## 11. Seguridad y secretos

Confirmación obligatoria:

- [ ] No se suben archivos `.env` reales
- [ ] No se suben tokens
- [ ] No se suben claves privadas
- [ ] No se suben credenciales
- [ ] No se suben bases SQLite locales
- [ ] No se suben artefactos temporales

---

## 12. Nota de alcance

Este PR debe mantener la separación entre Storefront público, Dashboard administrativo y backend modular.

Si el PR corresponde a una fase parcial, debe aclararse explícitamente qué queda pendiente para futuras ramas.

---

## 13. Checklist final

- [ ] El alcance del PR está claro
- [ ] El alcance excluido está claro
- [ ] Los archivos modificados corresponden al módulo indicado
- [ ] No se mezclan módulos sin justificación
- [ ] El build o test correspondiente fue ejecutado
- [ ] El PR está listo para revisión