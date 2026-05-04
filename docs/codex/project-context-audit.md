# Auditoría de Contexto del Proyecto — Always Beautiful

## 1. Propósito del documento

Este documento registra el contexto técnico actual del proyecto Always Beautiful para que Codex CLI, Codex App y futuros agentes puedan entender la arquitectura base antes de proponer cambios.

La finalidad es evitar que los agentes trabajen sin conocimiento del estado real del repositorio, de los módulos existentes, de las ramas activas y de los límites operativos del proyecto.

---

## 2. Estado Git al crear esta documentación

La documentación se creó desde la rama:

~~~text
feature/codex-operating-model
~~~

Antes de crear esta rama se preservó el avance local del Storefront con:

~~~bash
git stash push -u -m "wip(storefront): preservar avance local de home services antes de configurar codex"
~~~

El stash registrado fue:

~~~text
stash@{0}: On feature/storefront-home-services: wip(storefront): preservar avance local de home services antes de configurar codex
~~~

El objetivo de esta decisión fue evitar mezclar el avance visual del Storefront con la documentación operativa de Codex.

---

## 3. Rama actual de documentación

La rama `feature/codex-operating-model` tiene como objetivo documentar:

- Reglas operativas para Codex.
- Política GitFlow y Pull Requests.
- Plantillas de prompts.
- Protocolo de feedback.
- Inventario técnico.
- Roadmap de integraciones.
- Roadmap de IA.
- Sistema de marketing y Canva.

Esta rama no debe modificar lógica de frontend, backend ni módulos funcionales del producto.

---

## 4. Rama Storefront preservada

La rama `feature/storefront-home-services` contiene el avance local del Storefront.

Esa rama debe cerrarse más adelante como avance avanzado pausable, no como Storefront final al 100%.

Alcance pendiente de esa rama:

- Afinar Home.
- Afinar Services.
- Ordenar footer/franja inferior.
- Crear placeholders formales para Privacy y Terms.
- Ajustar responsive móvil.
- Ajustar responsive tablet.
- Validar shells públicos.
- Validar `/admin`.
- Ejecutar build.
- Separar commits.
- Crear Pull Requests.
- Fusionar hacia `develop` mediante merge commit.

---

## 5. Estructura general del proyecto

El proyecto tiene dos grandes superficies:

1. Backend modular en `services/api`.
2. Frontend React/Vite en `web`.

También contiene documentación técnica en `docs/` y configuración de Pull Requests en `.github/`.

---

## 6. Backend actual

El backend se encuentra en:

~~~text
services/api
~~~

Arquitectura actual:

- FastAPI.
- Pydantic.
- SQLAlchemy.
- pytest.
- Estructura modular por dominio.
- Separación por `routes.py`, `schemas.py`, `service.py` y `repository.py` cuando aplica.

Módulos backend detectados:

- `admin`
- `auth`
- `booking`
- `cart`
- `catalog`
- `core`
- `db`
- `notifications`
- `observability`
- `orders`
- `payments`
- `schedule`
- `shipping`

Archivo principal:

~~~text
services/api/app/main.py
~~~

---

## 7. Frontend actual

El frontend se encuentra en:

~~~text
web
~~~

Stack actual:

- React.
- Vite.
- JavaScript.
- React Router.
- CSS global.
- Layout administrativo.
- Layout público.

Archivos principales:

- `web/src/main.jsx`
- `web/src/App.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/index.css`
- `web/src/design/tokens.js`
- `web/src/layouts/AdminLayout.jsx`
- `web/src/layouts/PublicLayout.jsx`

---

## 8. Dashboard administrativo

El Dashboard administrativo se encuentra principalmente en:

~~~text
web/src/pages/admin/DashboardPage.jsx
web/src/components/EcommercePerformance.jsx
web/src/components/ExecutiveInsights.jsx
web/src/components/ProfessionalPerformance.jsx
web/src/components/TrendSnapshot.jsx
web/src/mockAdminData.js
~~~

Estado general:

- Dashboard visual avanzado.
- Métricas sintéticas.
- Componentes analíticos.
- Pendiente futura separación por secciones internas.
- Pendiente conexión más fuerte con datos reales.

No debe romperse por cambios del Storefront.

---

## 9. Storefront público

El Storefront público se encuentra principalmente en:

~~~text
web/src/pages/public/
web/src/layouts/PublicLayout.jsx
web/src/components/shared/PublicHeader.jsx
web/src/components/shared/PublicFooter.jsx
web/src/components/shared/StorefrontButton.jsx
web/src/components/shared/StorefrontCard.jsx
web/src/components/shared/SectionHeading.jsx
~~~

Páginas públicas detectadas:

- `HomePage.jsx`
- `ServicesPage.jsx`
- `ProductsPage.jsx`
- `BookingPage.jsx`
- `CartPage.jsx`
- `CheckoutPage.jsx`

Estado general:

- Base pública creada.
- Routing público preparado.
- Layout público separado.
- Design system inicial creado.
- Pendiente avance final de `feature/storefront-home-services`.

---

## 10. Documentación existente

Documentos actuales relevantes:

- `docs/00-vision.md`
- `docs/01-setup.md`
- `docs/storefront/00-module-scope.md`
- `docs/storefront/01-frontend-audit.md`
- `docs/storefront/02-guide-repo-map.md`
- `docs/storefront/03-data-request-checklist.md`

Documentos nuevos de la rama `feature/codex-operating-model`:

- `AGENTS.md`
- `.github/pull_request_template.md`
- `docs/codex/00-operating-model.md`
- `docs/codex/01-gitflow-pr-merge-policy.md`
- `docs/codex/02-task-prompt-templates.md`
- `docs/codex/03-feedback-protocol.md`
- `docs/codex/project-context-audit.md`
- `docs/architecture/00-project-modules-status.md`
- `docs/architecture/project-inventory.md`
- `docs/integrations/00-api-roadmap.md`
- `docs/ai/00-langchain-langgraph-roadmap.md`
- `docs/marketing/00-canva-content-system.md`

---

## 11. Archivos sensibles detectados

Archivos sensibles por impacto técnico:

- `.env.example`
- `services/api/.env.example`
- `services/api/app/main.py`
- `services/api/app/core/config.py`
- `services/api/app/auth/security.py`
- `services/api/requirements.txt`
- `web/package.json`
- `web/package-lock.json`
- `web/src/App.jsx`
- `web/src/main.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/index.css`
- `web/src/design/tokens.js`
- `web/src/layouts/AdminLayout.jsx`
- `web/src/layouts/PublicLayout.jsx`

---

## 12. Dependencias backend

El backend utiliza dependencias registradas en:

~~~text
services/api/requirements.txt
~~~

Dependencias principales:

- FastAPI.
- Starlette.
- Pydantic.
- Pydantic Settings.
- SQLAlchemy.
- Alembic.
- psycopg.
- pytest.
- PyJWT.
- argon2-cffi.
- email-validator.
- python-dotenv.
- uvicorn.

Codex no debe modificar `requirements.txt` sin autorización.

---

## 13. Dependencias frontend

El frontend utiliza dependencias registradas en:

~~~text
web/package.json
~~~

Dependencias principales:

- React.
- React DOM.
- React Router DOM.
- Vite.
- Plugin React para Vite.

Codex no debe modificar `package.json` ni `package-lock.json` sin autorización.

---

## 14. Estado de módulos del proyecto

Estado general aproximado:

- Foundation Layer: cerrado.
- Observability + Security: cerrado funcionalmente.
- Orders Core: avanzado.
- Payments Core: parcial.
- Shipping Core: parcial.
- Notifications: avanzado.
- Booking Engine: avanzado.
- Schedule Engine: pausado por datos reales.
- Catalog: avanzado.
- Cart + Checkout: parcial avanzado.
- Admin Panel Backend: muy avanzado.
- Admin Panel Frontend: avanzado con datos sintéticos.
- Storefront Experience: en implementación.
- Recommendation + Assistant Intelligence Layer: conceptual.

---

## 15. Próximas fases previstas

Orden de integración previsto:

1. Codex local seguro.
2. GitHub CLI.
3. Documentación técnica.
4. Frontend/backend.
5. APIs de negocio.
6. Canva.
7. IA.
8. AWS.

---

## 16. Riesgos principales del proyecto

Riesgos técnicos actuales:

- Mezclar documentación de Codex con avances visuales del Storefront.
- Romper `/admin` con cambios globales de CSS.
- Integrar APIs antes de tener sandbox.
- Instalar dependencias pesadas en MacBook Air 2017.
- Usar datos ficticios como si fueran datos reales.
- Crear commits demasiado grandes.
- Hacer push sin revisar `git status`.
- Aplicar stash en rama incorrecta.
- Modificar `main` directamente.
- Subir archivos temporales o secretos.

---

## 17. Regla de lectura para agentes

Antes de trabajar, Codex debe leer:

1. `AGENTS.md`
2. `docs/codex/00-operating-model.md`
3. `docs/codex/01-gitflow-pr-merge-policy.md`
4. `docs/codex/02-task-prompt-templates.md`
5. `docs/codex/03-feedback-protocol.md`
6. `docs/codex/project-context-audit.md`

Luego debe ejecutar diagnóstico antes de modificar cualquier archivo.

---

## 18. Conclusión

El proyecto Always Beautiful ya tiene una arquitectura modular seria y debe continuar con disciplina técnica.

La función de Codex será acelerar el desarrollo, pero sin reemplazar control humano, GitFlow, documentación, validaciones ni revisión de alcance.
