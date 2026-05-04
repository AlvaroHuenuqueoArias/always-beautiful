# Inventario Técnico del Proyecto — Always Beautiful

## 1. Propósito del documento

Este documento registra el inventario técnico del proyecto Always Beautiful Operations Platform.

Su objetivo es entregar una lectura estructurada del repositorio para Codex CLI, Codex App y futuros agentes técnicos, identificando:

- Estructura del proyecto.
- Superficies principales.
- Archivos importantes.
- Archivos sensibles.
- Dependencias backend.
- Dependencias frontend.
- Zonas de riesgo.
- Reglas de lectura antes de modificar código.

Este documento se diferencia del `README.md` porque no está orientado al usuario final ni a presentación general del proyecto. Está orientado a operación técnica, control de agentes, auditoría de cambios y protección de arquitectura.

---

## 2. Estructura general del repositorio

La estructura actual del proyecto es:

```text
.
├── .env.example
├── .github
│   └── pull_request_template.md
├── .gitignore
├── AGENTS.md
├── README.md
├── docs
│   ├── 00-vision.md
│   ├── 01-setup.md
│   ├── ai
│   │   └── 00-langchain-langgraph-roadmap.md
│   ├── architecture
│   │   ├── 00-project-modules-status.md
│   │   └── project-inventory.md
│   ├── codex
│   │   ├── 00-operating-model.md
│   │   ├── 01-gitflow-pr-merge-policy.md
│   │   ├── 02-task-prompt-templates.md
│   │   ├── 03-feedback-protocol.md
│   │   └── project-context-audit.md
│   ├── integrations
│   │   └── 00-api-roadmap.md
│   ├── marketing
│   │   └── 00-canva-content-system.md
│   └── storefront
│       ├── 00-module-scope.md
│       ├── 01-frontend-audit.md
│       ├── 02-guide-repo-map.md
│       └── 03-data-request-checklist.md
├── services
│   └── api
└── web
```

---

## 3. Superficies principales del sistema

El repositorio se divide en tres superficies principales:

### 3.1. Backend

Ubicación:

```text
services/api
```

Responsabilidad:

- API principal.
- Módulos de dominio.
- Auth.
- Seguridad.
- Observabilidad.
- Booking.
- Schedule.
- Catalog.
- Cart.
- Orders.
- Payments.
- Shipping.
- Notifications.
- Admin backend.

### 3.2. Frontend

Ubicación:

```text
web
```

Responsabilidad:

- Aplicación React/Vite.
- Dashboard administrativo.
- Storefront público.
- Layouts.
- Routing.
- Componentes compartidos.
- CSS global.
- Design tokens.

### 3.3. Documentación

Ubicación:

```text
docs
```

Responsabilidad:

- Visión.
- Setup.
- Storefront.
- Modelo operativo Codex.
- Arquitectura.
- Integraciones.
- IA.
- Marketing.

---

## 4. Inventario backend

### 4.1. Módulos backend detectados

```text
services/api/app/admin
services/api/app/auth
services/api/app/booking
services/api/app/cart
services/api/app/catalog
services/api/app/core
services/api/app/db
services/api/app/notifications
services/api/app/observability
services/api/app/orders
services/api/app/payments
services/api/app/schedule
services/api/app/shipping
```

### 4.2. Archivo principal backend

```text
services/api/app/main.py
```

Este archivo registra la aplicación FastAPI y conecta routers. Es sensible porque un cambio incorrecto puede romper múltiples módulos.

### 4.3. Configuración backend

```text
services/api/app/core/config.py
services/api/.env.example
.env.example
```

Estos archivos son sensibles porque definen configuración, variables y comportamiento por entorno.

### 4.4. Base de datos

```text
services/api/app/db/base.py
services/api/app/db/models.py
services/api/app/db/session.py
```

Estos archivos son sensibles porque afectan persistencia, modelos relacionales y sesiones de base de datos.

### 4.5. Tests backend

```text
services/api/tests/auth
services/api/tests/observability
services/api/tests/schedule
services/api/tests/conftest.py
```

---

## 5. Inventario frontend

### 5.1. Archivos principales

```text
web/src/main.jsx
web/src/App.jsx
web/src/app/AppRouter.jsx
web/src/index.css
web/src/design/tokens.js
web/vite.config.js
web/package.json
web/package-lock.json
```

### 5.2. Layouts

```text
web/src/layouts/AdminLayout.jsx
web/src/layouts/PublicLayout.jsx
```

### 5.3. Dashboard administrativo

```text
web/src/pages/admin/DashboardPage.jsx
web/src/components/EcommercePerformance.jsx
web/src/components/ExecutiveInsights.jsx
web/src/components/ProfessionalPerformance.jsx
web/src/components/TrendSnapshot.jsx
web/src/mockAdminData.js
```

### 5.4. Storefront público

```text
web/src/pages/public/HomePage.jsx
web/src/pages/public/ServicesPage.jsx
web/src/pages/public/ProductsPage.jsx
web/src/pages/public/BookingPage.jsx
web/src/pages/public/CartPage.jsx
web/src/pages/public/CheckoutPage.jsx
web/src/components/shared/PublicHeader.jsx
web/src/components/shared/PublicFooter.jsx
web/src/components/shared/SectionHeading.jsx
web/src/components/shared/StorefrontButton.jsx
web/src/components/shared/StorefrontCard.jsx
```

---

## 6. Archivos sensibles por impacto

Los siguientes archivos no deben modificarse sin autorización específica:

```text
web/src/index.css
web/src/design/tokens.js
web/src/App.jsx
web/src/main.jsx
web/src/app/AppRouter.jsx
web/src/layouts/AdminLayout.jsx
web/src/layouts/PublicLayout.jsx
web/package.json
web/package-lock.json
services/api/requirements.txt
services/api/app/main.py
services/api/app/core/config.py
services/api/app/db/session.py
services/api/app/auth/security.py
.env.example
services/api/.env.example
```

---

## 7. Archivos que no deben subirse

No deben ingresar a commits:

```text
node_modules/
dist/
.DS_Store
*.log
*.tmp
*.bak
*.old
web/full-project-tree.txt
.env reales
credenciales
tokens
claves privadas
bases SQLite locales
.pytest_cache/
coverage/
```

Nota: si `web/dist/` aparece en el repositorio, debe revisarse si fue versionado previamente o si debe ser limpiado en una rama específica. No eliminar sin analizar historial.

---

## 8. Dependencias backend

Archivo:

```text
services/api/requirements.txt
```

Dependencias principales detectadas:

```text
alembic==1.18.4
argon2-cffi==25.1.0
email-validator==2.3.0
fastapi==0.134.0
httpx==0.28.1
psycopg==3.3.3
psycopg-binary==3.3.3
pydantic==2.12.5
pydantic-settings==2.13.1
PyJWT==2.12.1
pytest==9.0.2
python-dotenv==1.2.2
SQLAlchemy==2.0.48
starlette==0.52.1
uvicorn==0.41.0
```

Codex no debe modificar dependencias backend sin aprobación.

---

## 9. Dependencias frontend

Archivo:

```text
web/package.json
```

Dependencias principales:

```text
react
react-dom
react-router-dom
vite
@vitejs/plugin-react
```

Scripts disponibles:

```text
npm --prefix web run dev
npm --prefix web run build
npm --prefix web run preview
```

Codex no debe modificar dependencias frontend sin aprobación.

---

## 10. Comandos de diagnóstico recomendados

Desde la raíz:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git log --oneline --graph --decorate -10
```

Inventario:

```bash
tree . -a -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|coverage|.pytest_cache|*.pyc|*.sqlite3|.DS_Store'
```

Frontend:

```bash
npm --prefix web run build
```

Backend:

```bash
cd services/api
source .venv/bin/activate
pytest
deactivate
cd ../..
```

---

## 11. Lectura por tipo de tarea

### Si la tarea es Storefront

Revisar:

- `docs/storefront/*`
- `docs/architecture/00-project-modules-status.md`
- `docs/codex/project-context-audit.md`
- `web/src/pages/public/*`
- `web/src/layouts/PublicLayout.jsx`
- `web/src/components/shared/*`

### Si la tarea es Dashboard

Revisar:

- `web/src/pages/admin/DashboardPage.jsx`
- `web/src/components/*`
- `web/src/mockAdminData.js`
- `docs/architecture/00-project-modules-status.md`

### Si la tarea es backend

Revisar:

- `services/api/app/main.py`
- módulo correspondiente en `services/api/app`
- tests relacionados

### Si la tarea es documentación Codex

Revisar:

- `AGENTS.md`
- `docs/codex/*`
- `.github/pull_request_template.md`

---

## 12. Riesgos técnicos actuales

Riesgos principales:

- Mezclar cambios de documentación con Storefront.
- Aplicar stash en rama incorrecta.
- Romper `/admin` con CSS global.
- Cambiar `tokens.js` sin revisar impacto.
- Integrar APIs externas sin sandbox.
- Instalar dependencias pesadas en MacBook Air 2017.
- Versionar archivos generados.
- Subir `.env` o secretos.
- Hacer PRs demasiado grandes.

---

## 13. Estado de trabajo preservado

Existe un stash asociado a la rama `feature/storefront-home-services`:

```text
stash@{0}: On feature/storefront-home-services: wip(storefront): preservar avance local de home services antes de configurar codex
```

No aplicar este stash dentro de `feature/codex-operating-model`.

---

## 14. Regla final

Antes de modificar archivos, Codex debe consultar este inventario para entender la estructura y detectar archivos sensibles.

Si una tarea puede afectar archivos críticos, debe solicitar autorización antes de actuar.
