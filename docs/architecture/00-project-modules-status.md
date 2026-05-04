# Estado Modular del Proyecto — Always Beautiful

## 1. Propósito del documento

Este documento registra el estado técnico y funcional de los módulos principales del proyecto Always Beautiful Operations Platform.

Su objetivo es entregar a Codex CLI, Codex App y futuros agentes técnicos una lectura clara del avance real del sistema antes de proponer cambios, crear ramas, modificar archivos o integrar nuevas funcionalidades.

Este documento no reemplaza el `README.md`. Su función es servir como mapa técnico de estado modular para decisiones de ingeniería, planificación de ramas, control de alcance, revisión de riesgos y priorización del trabajo.

---

## 2. Lectura ejecutiva del proyecto

Always Beautiful ya no debe ser tratado como un prototipo aislado. El proyecto posee una arquitectura fullstack modular compuesta por:

- Backend en FastAPI.
- Frontend en React/Vite.
- Dashboard administrativo interno.
- Storefront público.
- Módulos de dominio para reservas, agenda, catálogo, carrito, órdenes, pagos, envíos, notificaciones, seguridad y observabilidad.
- Roadmap futuro para IA conversacional, recomendaciones, Canva, WhatsApp, pagos online y AWS.

El proyecto debe avanzar mediante ramas específicas, commits separados, Pull Requests documentados y merge commits hacia `develop`.

---

## 3. Diferencia con documentación previa

Antes de integrar Codex, el proyecto ya tenía documentación de visión, setup y Storefront:

- `docs/00-vision.md`
- `docs/01-setup.md`
- `docs/storefront/00-module-scope.md`
- `docs/storefront/01-frontend-audit.md`
- `docs/storefront/02-guide-repo-map.md`
- `docs/storefront/03-data-request-checklist.md`

Esos documentos explican áreas específicas del proyecto.

Este documento tiene otra función: entregar una visión modular completa para que Codex no trabaje a ciegas ni confunda estados parciales con módulos cerrados.

---

## 4. Tabla maestra de módulos

| Nº | Módulo | Estado actual | Nivel aproximado | Depende de datos reales | Observación |
|---:|---|---|---:|---|---|
| 1 | Foundation Layer | Cerrado | 100% | No | Base técnica estable del sistema |
| 2 | Observability + Security | Cerrado funcional | 96% | No inmediato | Logging, métricas, headers, auth y roles básicos |
| 3 | Orders Core | Avanzado | 85% | Sí | Requiere conexión con checkout, pagos y envíos reales |
| 4 | Payments Core | Parcial | 35% | Sí | Falta proveedor real, sandbox y conciliación |
| 5 | Shipping Core | Parcial | 45% | Sí | Falta integración logística real |
| 6 | Notifications | Avanzado | 78% | No inmediato | Base event-driven creada |
| 7 | Booking Engine | Avanzado | 82% | Sí | Requiere reglas reales de negocio y agenda |
| 8 | Schedule Engine | Pausado parcial | 42% | Sí crítico | Depende de horarios, pausas y duraciones reales |
| 9 | Catalog | Avanzado | 75% | Sí | Requiere productos, fotos, categorías y precios reales |
| 10 | Cart + Checkout | Parcial avanzado | 60% | Sí | Falta checkout público real |
| 11 | Admin Panel Backend | Muy avanzado | 90% | Sí | Requiere datos reales para KPIs finales |
| 12 | Admin Panel Frontend | Avanzado | 82% | Sí | Dashboard visual con datos sintéticos |
| 13 | Storefront Experience | En implementación | 38–44% | Sí | Home, Services, routing y shells públicos en progreso |
| 14 | Recommendation + Assistant Intelligence Layer | Conceptual | 6% | Sí | Futuro asistente, IA y recomendaciones |

---

## 5. Módulo 1 — Foundation Layer

### Estado

Cerrado.

### Función

Establece la base técnica mínima del sistema:

- Backend inicial.
- Health check.
- CORS.
- Runtime estabilizado.
- Estructura inicial del repositorio.
- Base inicial de frontend.

### Archivos relacionados

- `services/api/app/main.py`
- `web/package.json`
- `web/vite.config.js`
- estructura raíz del proyecto

### Riesgo actual

Bajo.

### Regla para Codex

No modificar foundation salvo que una tarea de arquitectura lo justifique explícitamente.

---

## 6. Módulo 2 — Observability + Security

### Estado

Cerrado funcionalmente.

### Función

Entrega herramientas de seguridad y observabilidad:

- Rutas `/system`.
- Logging estructurado.
- Middleware.
- Request tracing.
- Headers de seguridad.
- Manejo global de errores.
- Autenticación administrativa.
- Roles básicos.
- Tests.

### Archivos relacionados

- `services/api/app/observability/*`
- `services/api/app/auth/*`
- `services/api/tests/observability/*`
- `services/api/tests/auth/*`

### Pendientes futuros

- Refresh/revoke tokens.
- Scopes más finos.
- Observabilidad externa.
- Hardening productivo.
- Monitoreo externo.

### Regla para Codex

No cambiar auth, seguridad o middleware sin tests y justificación.

---

## 7. Módulo 3 — Orders Core

### Estado

Avanzado.

### Función

Gestiona órdenes y estados de compra o reserva.

### Archivos relacionados

- `services/api/app/orders/routes.py`
- `services/api/app/orders/schemas.py`
- `services/api/app/orders/service.py`
- `services/api/app/orders/repository.py`

### Pendientes

- Conexión con Storefront.
- Conexión con pagos reales.
- Conexión con envíos reales.
- Experiencia pública de pedidos.

### Regla para Codex

No acoplar Orders directamente a proveedores externos. Usar adaptadores.

---

## 8. Módulo 4 — Payments Core

### Estado

Parcial.

### Función

Prepara la base para pagos y webhooks.

### Archivos relacionados

- `services/api/app/payments/client.py`
- `services/api/app/payments/routes.py`
- `services/api/app/payments/schemas.py`

### Pendientes

- Mercado Pago sandbox.
- PayPal sandbox.
- Abstracción de proveedor.
- Conciliación.
- Manejo de webhooks.
- Estados de pago.
- Integración con Orders.

### Regla para Codex

No integrar pagos productivos. Toda integración debe iniciar en sandbox.

---

## 9. Módulo 5 — Shipping Core

### Estado

Parcial.

### Función

Prepara estructura de cotización y envío.

### Archivos relacionados

- `services/api/app/shipping/client.py`
- `services/api/app/shipping/routes.py`
- `services/api/app/shipping/schemas.py`

### Pendientes

- Proveedor logístico real.
- Reglas comerciales.
- Zonas de despacho.
- Costos reales.
- Conexión con checkout.

### Regla para Codex

No conectar proveedor externo sin documentación y sandbox si aplica.

---

## 10. Módulo 6 — Notifications

### Estado

Avanzado.

### Función

Orquesta notificaciones y eventos.

### Archivos relacionados

- `services/api/app/notifications/routes.py`
- `services/api/app/notifications/schemas.py`
- `services/api/app/notifications/service.py`
- `services/api/app/notifications/repository.py`
- `services/api/app/notifications/dispatchers/email_dispatcher.py`
- `services/api/app/notifications/dispatchers/webhook_dispatcher.py`

### Pendientes

- Plantillas finales.
- Canal principal.
- Integración con reservas, órdenes, pagos y postventa.
- WhatsApp futuro.

### Regla para Codex

No enviar notificaciones reales sin canal y entorno controlado.

---

## 11. Módulo 7 — Booking Engine

### Estado

Avanzado.

### Función

Gestiona disponibilidad, slots, reservas y validación de solapamientos.

### Archivos relacionados

- `services/api/app/booking/*`

### Pendientes

- Integración con UI pública.
- Reglas reales de servicios.
- Duraciones reales.
- Profesionales reales.
- Políticas de cancelación.

### Regla para Codex

No cerrar booking funcional sin datos reales del negocio.

---

## 12. Módulo 8 — Schedule Engine

### Estado

Pausado parcial.

### Función

Define horarios, pausas, bloqueos y disponibilidad de operación.

### Archivos relacionados

- `services/api/app/schedule/*`
- `services/api/tests/schedule/*`

### Pendientes críticos

- Horarios reales.
- Pausas reales.
- Turnos reales.
- Días no laborales.
- Duración real por servicio.
- Restricciones por profesional.

### Regla para Codex

No inventar horarios ni duraciones. Este módulo depende de datos reales.

---

## 13. Módulo 9 — Catalog

### Estado

Avanzado.

### Función

Gestiona productos, servicios, filtros, estados e ítems comerciales.

### Archivos relacionados

- `services/api/app/catalog/*`

### Pendientes

- Imágenes reales.
- Categorías reales.
- Precios reales.
- Detalle de producto.
- Integración fuerte con Storefront.
- Relación producto-servicio.

### Regla para Codex

No publicar datos comerciales inventados como reales.

---

## 14. Módulo 10 — Cart + Checkout

### Estado

Parcial avanzado.

### Función

Gestiona carrito y transición futura al checkout.

### Archivos relacionados

- `services/api/app/cart/*`
- `web/src/pages/public/CartPage.jsx`
- `web/src/pages/public/CheckoutPage.jsx`

### Pendientes

- Checkout público real.
- Integración con pagos.
- Integración con envíos.
- Validación de datos del cliente.
- Confirmación de orden.

### Regla para Codex

No cerrar checkout hasta tener pagos, envío y reglas comerciales definidas.

---

## 15. Módulo 11 — Admin Panel Backend

### Estado

Muy avanzado.

### Función

Expone métricas, agregaciones y resumen ejecutivo para administración.

### Archivos relacionados

- `services/api/app/admin/routes.py`
- `services/api/app/admin/schemas.py`
- `services/api/app/admin/service.py`

### Pendientes

- Métricas con datos reales.
- Políticas de permisos más finas.
- KPIs finales.
- Integración con datos operativos reales.

### Regla para Codex

No alterar métricas administrativas sin validar impacto en Dashboard.

---

## 16. Módulo 12 — Admin Panel Frontend

### Estado

Avanzado.

### Función

Entrega Dashboard visual administrativo con métricas sintéticas.

### Archivos relacionados

- `web/src/pages/admin/DashboardPage.jsx`
- `web/src/components/EcommercePerformance.jsx`
- `web/src/components/ExecutiveInsights.jsx`
- `web/src/components/ProfessionalPerformance.jsx`
- `web/src/components/TrendSnapshot.jsx`
- `web/src/mockAdminData.js`

### Pendientes

- Separar métricas por botones.
- Crear navegación interna del Dashboard.
- Reducir dependencia de datos sintéticos.
- Integrar datos reales.
- Permisos visuales por rol.

### Regla para Codex

Trabajar Dashboard en ramas propias, no dentro de ramas Storefront.

---

## 17. Módulo 13 — Storefront Experience

### Estado

En implementación.

### Función

Construye la experiencia pública para clientas:

- Home.
- Services.
- Products.
- Booking.
- Cart.
- Checkout.
- Footer.
- Header.
- Botón flotante.
- Futuro asistente.

### Archivos relacionados

- `web/src/layouts/PublicLayout.jsx`
- `web/src/components/shared/PublicHeader.jsx`
- `web/src/components/shared/PublicFooter.jsx`
- `web/src/components/shared/StorefrontButton.jsx`
- `web/src/components/shared/StorefrontCard.jsx`
- `web/src/components/shared/SectionHeading.jsx`
- `web/src/pages/public/*`
- `web/src/index.css`
- `web/src/design/tokens.js`

### Pendientes inmediatos

- Recuperar stash de `feature/storefront-home-services`.
- Afinar Home.
- Afinar Services.
- Footer institucional.
- Privacy/Terms placeholders.
- Responsive móvil/tablet.
- Validar `/admin`.
- Build.
- Separar commits.

### Regla para Codex

Cerrar esta rama como avance avanzado pausable, no como Storefront final.

---

## 18. Módulo 14 — Recommendation + Assistant Intelligence Layer

### Estado

Conceptual.

### Función

Futuro módulo de inteligencia para:

- Asistente conversacional.
- Memoria.
- Recomendaciones.
- Cross-sell.
- Bundles.
- WhatsApp.
- LangChain.
- LangGraph.

### Pendientes

- Diseñar arquitectura.
- Definir datos base.
- Crear reglas determinísticas.
- Crear assistant endpoint.
- Diseñar memoria.
- Integrar catálogo.
- Evaluar LangGraph.
- Evaluar WhatsApp real.

### Regla para Codex

No implementar IA avanzada sin datos, contratos de backend y alcance específico.

---

## 19. Módulos dependientes de datos reales

Estos módulos no pueden cerrarse productivamente sin información real del negocio:

- Schedule Engine.
- Booking Engine.
- Catalog.
- Cart + Checkout.
- Payments Core.
- Shipping Core.
- Admin Panel Backend.
- Admin Panel Frontend.
- Storefront Experience.
- Assistant Intelligence.

---

## 20. Módulos que pueden avanzar con documentación o estructura

Pueden avanzar sin datos reales definitivos:

- Codex Operating Model.
- GitFlow policy.
- Project inventory.
- API roadmap.
- IA roadmap.
- Marketing/Canva system.
- Dashboard navigation shell.
- Storefront responsive base.
- Legal placeholders no definitivos.

---

## 21. Prioridad técnica recomendada

Orden recomendado posterior a esta rama de documentación:

1. Cerrar `feature/codex-operating-model`.
2. Volver a `feature/storefront-home-services`.
3. Recuperar stash del Storefront.
4. Cerrar avance avanzado pausable del Storefront.
5. Crear PR hacia `develop`.
6. Decidir siguiente rama:
   - `feature/admin-dashboard-navigation`, o
   - `feature/storefront-catalog-commercial`.

---

## 22. Regla final

Codex debe consultar este documento antes de proponer cambios de arquitectura, módulos, APIs, IA o Dashboard.

Si una tarea afecta más de un módulo, debe explicarse por qué antes de modificar archivos.