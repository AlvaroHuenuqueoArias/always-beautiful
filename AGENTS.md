# AGENTS.md — Always Beautiful Operations Platform

## Propósito del archivo

Este archivo define las reglas operativas obligatorias para Codex CLI, Codex App y cualquier agente de asistencia técnica que trabaje dentro del repositorio `always-beautiful`.

El objetivo es proteger la arquitectura actual del proyecto, mantener GitFlow coherente, evitar cambios no autorizados, impedir modificaciones destructivas y garantizar que cada avance sea profesional, auditable y validado.

Codex no debe actuar como un agente libre. Codex debe actuar como un ejecutor técnico bajo instrucciones explícitas, con alcance definido, validaciones obligatorias y revisión humana antes de commits, push, Pull Requests o merge commits.

---

## Regla 1 — Identidad del proyecto

Always Beautiful es una plataforma fullstack modular para la operación profesional de un salón de belleza.

El sistema está diseñado como una plataforma empresarial compuesta por:

- Storefront público para clientas.
- Dashboard administrativo interno.
- Backend modular con FastAPI.
- Frontend con React y Vite.
- Módulos de reservas, agenda, catálogo, carrito, pagos, envíos, notificaciones, seguridad y observabilidad.
- Futuras integraciones con IA conversacional, recomendaciones, WhatsApp, Canva, pagos online y AWS.

El proyecto debe mantenerse con lógica académica, empresarial, auditable y profesional.

---

## Regla 2 — Stack técnico actual

### Backend

- Python.
- FastAPI.
- SQLAlchemy.
- Pydantic.
- Pydantic Settings.
- pytest.
- PostgreSQL como objetivo productivo.
- SQLite o persistencia local solo para pruebas cuando aplique.
- Arquitectura modular por dominio.
- Separación por `routes.py`, `schemas.py`, `service.py` y `repository.py` cuando aplica.

### Frontend

- React.
- Vite.
- JavaScript.
- React Router.
- CSS global controlado.
- Layout público para Storefront.
- Layout administrativo para Dashboard.
- Componentes compartidos.
- Design tokens.

### Git

- `main` como rama estable.
- `develop` como rama de integración.
- `feature/*` para nuevas funcionalidades.
- `fix/*` para correcciones.
- `release/*` para cierres de versión.
- Merge commits obligatorios para mantener trazabilidad histórica.

---

## Regla 3 — Estructura actual del proyecto

La estructura base actual del repositorio es:

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
│       ├── .env.example
│       ├── .gitignore
│       ├── app
│       │   ├── __init__.py
│       │   ├── admin
│       │   ├── auth
│       │   ├── booking
│       │   ├── cart
│       │   ├── catalog
│       │   ├── core
│       │   ├── db
│       │   ├── main.py
│       │   ├── notifications
│       │   ├── observability
│       │   ├── orders
│       │   ├── payments
│       │   ├── schedule
│       │   └── shipping
│       ├── pytest.ini
│       ├── requirements.txt
│       └── tests
│           ├── auth
│           ├── conftest.py
│           ├── observability
│           └── schedule
└── web
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── images
    │       └── storefront
    │           └── home
    ├── src
    │   ├── App.jsx
    │   ├── app
    │   │   └── AppRouter.jsx
    │   ├── components
    │   │   ├── EcommercePerformance.jsx
    │   │   ├── ExecutiveInsights.jsx
    │   │   ├── ProfessionalPerformance.jsx
    │   │   ├── TrendSnapshot.jsx
    │   │   └── shared
    │   ├── data
    │   │   └── storefront
    │   ├── design
    │   │   └── tokens.js
    │   ├── index.css
    │   ├── layouts
    │   │   ├── AdminLayout.jsx
    │   │   └── PublicLayout.jsx
    │   ├── main.jsx
    │   ├── mockAdminData.js
    │   └── pages
    │       ├── admin
    │       └── public
    └── vite.config.js
```

---

## Regla 4 — Archivos y carpetas importantes

Los siguientes archivos y carpetas son estratégicos para el proyecto y deben tratarse con especial cuidado.

### Documentación principal

- `README.md`
- `AGENTS.md`
- `.github/pull_request_template.md`
- `docs/00-vision.md`
- `docs/01-setup.md`
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
- `docs/storefront/00-module-scope.md`
- `docs/storefront/01-frontend-audit.md`
- `docs/storefront/02-guide-repo-map.md`
- `docs/storefront/03-data-request-checklist.md`

### Backend

- `services/api/app/main.py`
- `services/api/app/core/config.py`
- `services/api/app/db/session.py`
- `services/api/app/db/models.py`
- `services/api/app/auth/*`
- `services/api/app/admin/*`
- `services/api/app/booking/*`
- `services/api/app/catalog/*`
- `services/api/app/cart/*`
- `services/api/app/orders/*`
- `services/api/app/payments/*`
- `services/api/app/shipping/*`
- `services/api/app/notifications/*`
- `services/api/app/observability/*`
- `services/api/requirements.txt`
- `services/api/pytest.ini`
- `services/api/tests/*`

### Frontend

- `web/package.json`
- `web/package-lock.json`
- `web/vite.config.js`
- `web/src/main.jsx`
- `web/src/App.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/index.css`
- `web/src/design/tokens.js`
- `web/src/layouts/AdminLayout.jsx`
- `web/src/layouts/PublicLayout.jsx`
- `web/src/pages/admin/DashboardPage.jsx`
- `web/src/pages/public/HomePage.jsx`
- `web/src/pages/public/ServicesPage.jsx`
- `web/src/pages/public/ProductsPage.jsx`
- `web/src/pages/public/BookingPage.jsx`
- `web/src/pages/public/CartPage.jsx`
- `web/src/pages/public/CheckoutPage.jsx`
- `web/src/components/shared/*`
- `web/src/components/storefront/*`
- `web/src/data/storefront/*`
- `web/public/images/storefront/home/*`

---

## Regla 5 — Archivos sensibles

Los siguientes archivos son sensibles por nombre, ubicación o impacto técnico:

- `.env.example`
- `services/api/.env.example`
- `web/src/design/tokens.js`
- `web/src/index.css`
- `web/src/App.jsx`
- `web/src/main.jsx`
- `web/src/layouts/AdminLayout.jsx`
- `web/src/layouts/PublicLayout.jsx`
- `web/package.json`
- `web/package-lock.json`
- `services/api/requirements.txt`
- `services/api/app/core/config.py`
- `services/api/app/db/session.py`
- `services/api/app/auth/security.py`

Codex no debe modificar estos archivos sin explicar previamente el motivo técnico, el riesgo, el alcance y la validación necesaria.

---

## Regla 6 — Dependencias backend oficiales

Las dependencias backend actuales están definidas en `services/api/requirements.txt`.

Dependencias principales detectadas:

```text
alembic==1.18.4
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.1
argon2-cffi==25.1.0
argon2-cffi-bindings==25.1.0
certifi==2026.2.25
cffi==2.0.0
click==8.3.1
dnspython==2.8.0
email-validator==2.3.0
fastapi==0.134.0
greenlet==3.3.2
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.11
iniconfig==2.3.0
Mako==1.3.10
MarkupSafe==3.0.3
packaging==26.0
pluggy==1.6.0
psycopg==3.3.3
psycopg-binary==3.3.3
pwdlib==0.3.0
pycparser==3.0
pydantic==2.12.5
pydantic-settings==2.13.1
pydantic_core==2.41.5
Pygments==2.19.2
PyJWT==2.12.1
pytest==9.0.2
python-dotenv==1.2.2
SQLAlchemy==2.0.48
starlette==0.52.1
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.41.0
```

Codex no debe instalar, actualizar ni eliminar dependencias backend sin autorización explícita.

---

## Regla 7 — Dependencias frontend oficiales

Las dependencias frontend actuales están definidas en `web/package.json`.

```json
{
  "name": "always-beautiful-web",
  "private": true,
  "version": "0.1.0",
  "description": "Frontend oficial Always Beautiful",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "author": "Always Beautiful",
  "license": "UNLICENSED",
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "react-router-dom": "^7.14.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^6.0.1",
    "vite": "^8.0.0"
  }
}
```

Codex no debe modificar `package.json` ni `package-lock.json` sin autorización explícita.

Antes de instalar cualquier paquete frontend, Codex debe explicar:

1. Qué paquete propone.
2. Para qué se usará.
3. Qué archivo modificará.
4. Qué alternativa existe sin instalar dependencias.
5. Qué riesgo tiene para el proyecto.
6. Qué validación se ejecutará después.

---

## Regla 8 — Reglas obligatorias de Git

Codex debe respetar estrictamente estas reglas:

- Usar `git checkout`, no `git switch`.
- No crear ramas nuevas sin autorización explícita.
- No hacer squash.
- Mantener merge commits.
- No eliminar ramas sin autorización.
- No hacer push sin autorización explícita.
- No tocar `main` directamente.
- Integrar cambios hacia `develop` mediante Pull Request.
- Usar mensajes en español formal con estilo Conventional Commits.
- Antes de cualquier commit, ejecutar o solicitar `git status --short`.
- Después de cualquier commit, ejecutar o solicitar `git log --oneline --graph --decorate -10`.

Ejemplos válidos:

- `feat(storefront): estructurar footer institucional y páginas legales iniciales`
- `style(storefront): adaptar experiencia pública a móvil y tablet`
- `docs(codex): documentar modelo operativo para agentes de desarrollo`
- `docs(architecture): registrar inventario técnico del proyecto`
- `test(api): validar rutas protegidas del backend`

---

## Regla 9 — Comandos de diagnóstico obligatorios

Antes de modificar archivos, Codex debe ejecutar o solicitar:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git log --oneline --graph --decorate -10
```

Para inspección estructural del proyecto:

```bash
tree . -a -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|coverage|.pytest_cache|*.pyc|*.sqlite3|.DS_Store'
```

Para frontend:

```bash
npm --prefix web run build
```

Para backend, solo cuando la tarea toque `services/api`:

```bash
cd services/api
source .venv/bin/activate
pytest
deactivate
cd ../..
```

---

## Regla 10 — Reglas de protección del código existente

El código actual se considera una base optimizada y no debe reescribirse sin autorización.

Codex NO debe:

- Reescribir componentes completos sin autorización.
- Cambiar dimensiones globales sin autorización.
- Cambiar colores base sin autorización.
- Cambiar layout del Dashboard cuando trabaja en Storefront.
- Cambiar layout del Storefront cuando trabaja en Dashboard.
- Cambiar rutas existentes sin explicar impacto.
- Modificar `App.jsx`, `main.jsx` o layouts globales sin justificarlo.
- Mover, borrar o renombrar assets públicos sin autorización.
- Convertir mocks en datos reales inventados.
- Instalar dependencias sin aprobación.
- Modificar archivos `.env` reales.
- Exponer credenciales, tokens, claves privadas o datos sensibles.
- Ejecutar comandos destructivos sin aprobación explícita.
- Hacer refactors masivos sin autorización.
- Mezclar cambios de módulos no relacionados.

Codex SÍ puede:

- Auditar código.
- Proponer cambios.
- Crear documentación.
- Crear páginas placeholder formales.
- Ajustar responsive dentro de archivos autorizados.
- Ejecutar build/tests cuando esté autorizado.
- Preparar mensajes de commit y PR.
- Recomendar separación de commits.
- Detectar riesgos de arquitectura.
- Proponer mejoras sin aplicarlas automáticamente.

---

## Regla 11 — Archivos que no deben subirse

No incluir en commits:

- `node_modules/`
- `dist/`
- `.DS_Store`
- `*.log`
- `*.tmp`
- `*.bak`
- `*.old`
- `web/full-project-tree.txt`
- archivos `.env` reales
- credenciales
- tokens
- claves privadas
- bases SQLite locales
- artefactos de caché
- `.pytest_cache/`
- `coverage/`
- archivos generados no solicitados

Si Codex detecta estos archivos en `git status`, debe advertirlo antes de cualquier commit.

---

## Regla 12 — Reglas para Storefront

La rama `feature/storefront-home-services` debe cerrarse como avance avanzado pausable, no como Storefront final al 100%.

Alcance permitido en esa rama:

- Home pública.
- Services pública.
- PublicHeader.
- PublicFooter.
- PublicLayout.
- Tokens visuales.
- CSS responsive.
- Páginas placeholder para Privacy y Terms.
- Shells públicos navegables.
- Data mock claramente separada.
- Assets públicos del Storefront.

Fuera de alcance en esa rama:

- Mercado Pago.
- PayPal.
- Checkout real.
- Booking real.
- WhatsApp real.
- LangChain.
- LangGraph.
- Machine Learning.
- AWS.
- Docker productivo.
- Base de datos productiva.
- Datos reales definitivos del negocio.

La rama puede cerrarse si cumple:

- Home se ve profesional en desktop.
- Home se ve aceptable en móvil.
- Home se ve aceptable en tablet.
- Services se ve profesional en desktop.
- Services se ve aceptable en móvil/tablet.
- Footer o franja inferior tiene estructura ordenada.
- Existen enlaces o placeholders formales para Privacy y Terms.
- Products, Booking, Cart y Checkout cargan como shells.
- `/admin` no se rompe.
- Build frontend pasa.
- Git status queda limpio después de commits.
- PRs quedan separados por categoría.

### Restricción visual crítica — `hero-effect2.png`

En el módulo Storefront, la imagen correcta del efecto visual es:

```text
web/public/images/storefront/home/hero-effect2.png
```

La referencia pública correcta desde React/Vite es:

```text
/images/storefront/home/hero-effect2.png
```

Contexto técnico:

- Se detectó previamente una referencia incorrecta a `hero-effect1.png`.
- El archivo `hero-effect1.png` no existe en `web/public/images/storefront/home/`.
- El archivo correcto sí existe y se llama `hero-effect2.png`.
- Luego de corregir el nombre, se detectó una duplicación visual donde `hero-effect2.png` aparecía como una capa suelta en la esquina superior izquierda del Home.
- Esa duplicación rompía la composición visual del hero superior y no debe reintroducirse.

Regla obligatoria:

Codex no debe volver a insertar una capa directa de background con `hero-effect2.png` sobre el Home superior.

Codex no debe reintroducir reglas CSS de este tipo en capas superiores del Home:

```css
background: url("/images/storefront/home/hero-effect2.png") center center /
  contain no-repeat;
```

Si Codex necesita usar `hero-effect2.png`, debe hacerlo únicamente dentro de las capas visuales ya existentes, sin duplicar el hero, sin crear una imagen flotante adicional, sin posicionarla en la esquina superior izquierda y sin romper el diseño desktop ya aprobado.

Antes de modificar `web/src/index.css`, `HomePage.jsx`, `HeroSection.jsx` o cualquier componente visual del Storefront que use assets del Home, Codex debe revisar si el cambio puede afectar:

- Hero superior.
- Capas visuales del Home.
- Responsive móvil/tablet.
- PublicLayout.
- Dashboard administrativo.
- Composición visual aprobada.

Si existe riesgo visual, Codex debe detenerse, explicar el riesgo y pedir autorización antes de modificar.

---

## Regla 13 — Reglas para Dashboard

El Dashboard administrativo no debe romperse por cambios del Storefront.

Si una tarea modifica:

- `web/src/index.css`
- `web/src/App.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/layouts/*`
- `web/src/components/shared/*`
- `web/src/design/tokens.js`

Codex debe advertir el riesgo y validar que `/admin` no quede afectado.

El Dashboard debe evolucionar en futuras ramas para separar:

- Inicio del Dashboard.
- Ventas.
- Reservas.
- Productos.
- Pagos.
- Clientas.
- Marketing.
- IA / Insights.
- Configuración.

No debe mezclarse esa evolución con la rama actual del Storefront.

---

## Regla 14 — Reglas para documentación

Toda decisión técnica relevante debe quedar documentada en:

- `README.md`
- `docs/`
- descripción del Pull Request

La documentación debe estar en español formal, con lógica técnica clara y estilo profesional.

Toda documentación debe diferenciar entre:

- Funcionalidad cerrada.
- Funcionalidad avanzada pero parcial.
- Funcionalidad mock.
- Funcionalidad futura.
- Funcionalidad pendiente de datos reales.
- Funcionalidad pendiente de integración externa.

---

## Regla 15 — Reglas para Pull Requests

Todo Pull Request debe incluir:

- Resumen.
- Alcance incluido.
- Alcance excluido.
- Módulo afectado.
- Validaciones ejecutadas.
- Riesgos revisados.
- Decisiones técnicas.
- Nota de alcance.

No se deben crear PRs gigantes que mezclen módulos no relacionados.

No se debe hacer squash.

Los merges deben conservar merge commit cuando el flujo del proyecto lo requiera.

---

## Regla 16 — Reglas para APIs externas

No integrar APIs reales sin rama específica, sandbox, documentación y aprobación previa.

Futuras APIs previstas:

- Mercado Pago.
- PayPal.
- Canva Connect API.
- WhatsApp Business / Meta.
- AWS.
- Servicios de email o notificaciones.

Toda integración debe seguir este orden:

1. Documentación.
2. Sandbox.
3. `.env.example`.
4. Adaptador interno.
5. Tests.
6. Webhook si corresponde.
7. PR independiente.
8. Producción solo con aprobación.

No se deben usar credenciales productivas en desarrollo local sin autorización explícita.

No se deben pegar tokens en código fuente.

No se deben subir secretos a Git.

---

## Regla 17 — Reglas para IA

No implementar LangChain, LangGraph, memoria, WhatsApp o recomendaciones inteligentes sin una rama específica.

Orden futuro recomendado:

1. Assistant endpoint básico.
2. Session ID.
3. Memoria corta.
4. Reglas determinísticas.
5. Catálogo consultable.
6. LangGraph.
7. Memoria persistente.
8. WhatsApp real.

La recomendación de productos debe comenzar con reglas determinísticas antes de Machine Learning real.

No se debe prometer efectividad cosmética, médica o científica sin fuentes confiables.

---

## Regla 18 — Reglas para Canva y marketing

Canva se usará inicialmente como herramienta de producción visual y comercial.

Codex puede ayudar a crear:

- Calendario editorial.
- Copies.
- Guiones de reels.
- Prompts visuales.
- Sistema de campañas.
- Naming de assets.
- Briefs de diseño.
- Documentación para Canva.

Codex no debe asumir que puede editar Canva directamente si no existe una integración configurada.

Canva Connect API queda para una fase futura con documentación y rama específica.

---

## Regla 19 — Reglas para AWS y despliegue

No implementar AWS, Docker, RDS, EC2, ECS, CloudWatch, Secrets Manager o despliegues productivos sin fase específica.

El MacBook Air 2017 tiene limitaciones reales de hardware, por lo que no se deben instalar herramientas pesadas ni ejecutar Docker productivo localmente sin autorización.

La arquitectura AWS futura debe documentarse antes de implementarse.

Toda infraestructura debe considerar:

- Costos.
- Seguridad.
- IAM mínimo.
- Variables de entorno.
- Gestión de secretos.
- Observabilidad.
- Rollback.
- Separación entre desarrollo y producción.

---

## Regla 20 — Protocolo de feedback de Codex

Antes de modificar archivos, Codex debe entregar:

- Rama actual.
- Estado Git.
- Archivos modificados.
- Archivos nuevos.
- Riesgos.
- Archivos que tocará.
- Archivos que no tocará.
- Comandos que ejecutará.

Después de modificar archivos, Codex debe entregar:

- Archivos modificados.
- Archivos creados.
- Comandos ejecutados.
- Build/tests ejecutados.
- Resultado.
- Riesgos pendientes.
- Siguiente paso recomendado.
- Commit sugerido.
- PR sugerido si aplica.

Codex debe detenerse si necesita tocar archivos fuera del alcance autorizado.

---

## Regla 21 — Regla final de operación

Si un cambio puede afectar una base estable, Codex debe detenerse, explicar el riesgo y pedir autorización antes de modificar.

Codex no mejora libremente.

Codex ejecuta cambios autorizados, en archivos autorizados, con validación obligatoria y feedback técnico.

El usuario mantiene la dirección técnica del proyecto. Codex actúa como ejecutor técnico controlado.

---

## Regla 22 — Orquestación de IA con Codex CLI y DeepSeek

Este repositorio puede ser asistido por tres IA operativas: Codex CLI, DeepSeek V4 Flash y DeepSeek V4 Pro. Todos los agentes deben respetar este archivo `AGENTS.md` como fuente principal de gobernanza técnica.

Gemini/OpenRouter queda pausado como agente operativo debido a límites de créditos y `max_tokens` en OpenRouter. No debe considerarse parte del flujo activo hasta que el usuario confirme que OpenRouter puede usarse de forma estable.

### 22.1 Jerarquía oficial de agentes

1. Codex CLI / OpenAI Plus
   Rol: Principal Fullstack Software Engineer.
   Autoridad: máxima autoridad técnica para cambios complejos, arquitectura, integración final, revisión de Pull Requests y cierre de decisiones críticas.

2. DeepSeek V4 Flash vía OpenCode
   Rol: Backend Developer / Backend Debugging Assistant.
   Alcance: FastAPI, Python, Pydantic, SQLAlchemy, rutas, schemas, services, repositories, pytest, curl y diagnóstico de errores backend.
   Configuración recomendada: DeepSeek V4 Flash con effort Medium para uso diario.

3. DeepSeek V4 Pro vía OpenCode
   Rol: Frontend Advanced / Architecture Reviewer.
   Alcance: React, Vite, CSS controlado, Storefront público, assistant UI, booking conversion flow, revisión de contratos frontend-backend, transición assistant → cart y problemas complejos de integración.
   Configuración recomendada: DeepSeek V4 Pro con effort Medium para revisión avanzada y High solo en problemas complejos.

### 22.2 Regla central de trabajo

Una sola IA puede modificar archivos por turno.

Las demás IA pueden leer, diagnosticar, revisar, planificar o auditar, pero no deben modificar archivos al mismo tiempo en la misma rama.

Codex CLI conserva la autoridad técnica final.

### 22.3 Codex CLI

Codex CLI es el agente principal.

Debe usarse para:

- arquitectura compleja
- integración frontend/backend
- decisiones de software engineering
- refactors grandes
- pagos/envíos reales
- seguridad
- assistant intelligence avanzada
- LangChain/LangGraph
- Machine Learning
- preparación final de Pull Requests
- revisión final de cambios hechos por DeepSeek
- decisión de commit
- decisión de push
- decisión de Pull Request
- cierre técnico de rama

Codex CLI no debe actuar como agente libre. Debe revisar el handoff, explicar riesgos y solicitar autorización antes de modificar archivos sensibles.

### 22.4 DeepSeek V4 Flash — Backend

DeepSeek V4 Flash debe usarse como agente auxiliar técnico de backend, debugging y validaciones.

Puede trabajar en:

- `services/api/app/assistant/*`
- `services/api/app/assistant/tools/*`
- `services/api/app/booking/*`
- `services/api/app/catalog/*`
- `services/api/app/cart/*`
- `services/api/app/orders/*`
- `services/api/app/schedule/*`
- `services/api/app/notifications/*`
- `services/api/tests/*`

Puede ejecutar, con autorización:

```bash
cd services/api
source .venv/bin/activate
pytest
deactivate
cd ../..
git status --short
```

No debe tocar frontend visual salvo autorización explícita.

No debe modificar:

- `web/*`
- `AGENTS.md`
- `.env`
- `services/api/requirements.txt`
- `web/package.json`
- `web/package-lock.json`
- archivos de configuración sensible
- archivos de Git
- documentación estratégica salvo autorización explícita

### 22.5 DeepSeek V4 Pro — Frontend avanzado / arquitectura

DeepSeek V4 Pro debe usarse como agente auxiliar para frontend avanzado, revisión de arquitectura y problemas complejos.

Puede diagnosticar o modificar, con autorización:

- `web/src/services/assistantClient.js`
- `web/src/components/shared/AssistantChatPanel.jsx`
- `web/src/components/shared/AssistantChatWidget.jsx`
- `web/src/components/shared/AssistantComposer.jsx`
- `web/src/components/shared/AssistantMessageList.jsx`
- `web/src/components/shared/FloatingAssistantButton.jsx`
- `web/src/components/shared/PublicHeader.jsx`
- `web/src/pages/public/CartPage.jsx`
- `web/src/pages/public/BookingPage.jsx`
- `web/src/pages/public/CheckoutPage.jsx`
- `web/src/pages/public/ProductsPage.jsx`
- `web/src/pages/public/ServicesPage.jsx`
- `web/src/components/storefront/*`
- `web/src/layouts/PublicLayout.jsx`
- `web/src/data/storefront/*`
- `web/src/index.css` solo con autorización explícita

Puede ejecutar, con autorización:

```bash
npm --prefix web run build
git diff --check
git status --short
```

No debe tocar backend salvo autorización explícita.

No debe modificar:

- `services/api/*` sin autorización explícita
- `AGENTS.md`
- `.env`
- `web/package.json`
- `web/package-lock.json`
- dependencias
- archivos de configuración sensible
- archivos Git
- Dashboard administrativo salvo autorización explícita

### 22.6 OpenRouter/Gemini — Estado pausado

Gemini 3 Flash Preview vía OpenCode + OpenRouter queda pausado como agente operativo.

Motivo:

- OpenRouter devolvió error de créditos/max_tokens.
- El flujo gratuito no es estable para el nivel de contexto requerido por este repositorio.
- El proyecto no debe depender de una IA que no puede ejecutar diagnósticos largos de forma confiable.

Gemini/OpenRouter podrá reactivarse solo si el usuario confirma que:

- OpenRouter tiene créditos suficientes.
- La API key no tiene límites restrictivos.
- El modelo seleccionado funciona con prompts largos.
- No afecta el flujo operativo principal.

Mientras esté pausado:

- no debe aparecer como agente activo
- no debe recibir tareas críticas
- no debe ser requisito para avanzar
- no debe bloquear decisiones de DeepSeek o Codex

### 22.7 Prohibiciones para todos los agentes

Ningún agente puede ejecutar sin autorización explícita:

- `git add`
- `git commit`
- `git push`
- `git merge`
- `git reset --hard`
- `git clean`
- `git branch -D`
- crear Pull Request
- cerrar Pull Request
- mergear Pull Request
- instalar dependencias
- editar `.env`
- modificar credenciales
- tocar `package.json`
- tocar `package-lock.json`
- tocar `requirements.txt`
- ejecutar curl’s manuales sin autorización
- modificar archivos sensibles fuera del alcance autorizado

### 22.8 Archivos obligatorios de coordinación

Antes de trabajar, todo agente debe leer:

- `AGENTS.md`
- `docs/ai-handoff/ACTIVE_CONTEXT.md`
- `docs/ai-handoff/AGENT_ROLES.md`
- `docs/ai-handoff/CHANGELOG_AI.md`

Si el agente trabaja frontend, debe leer también:

- `docs/ai-handoff/FRONTEND_HANDOFF.md`

Si el agente trabaja backend, debe leer también:

- `docs/ai-handoff/BACKEND_HANDOFF.md`

Si Codex CLI debe retomar trabajo después de DeepSeek, se debe actualizar:

- `docs/ai-handoff/CODEX_REENTRY.md`

### 22.9 Registro obligatorio

Después de cada diagnóstico, implementación, fix o validación, el agente debe actualizar:

- `docs/ai-handoff/CHANGELOG_AI.md`
- `docs/ai-handoff/ACTIVE_CONTEXT.md`

Debe registrar:

- fecha y hora
- modelo usado
- herramienta usada
- rama actual
- archivos leídos
- archivos modificados
- comandos ejecutados
- resultado de build/test/curl
- errores encontrados
- riesgos pendientes
- siguiente paso recomendado
- si Codex CLI debe revisar algo

Si el trabajo fue backend, debe actualizar también:

- `docs/ai-handoff/BACKEND_HANDOFF.md`

Si el trabajo fue frontend, debe actualizar también:

- `docs/ai-handoff/FRONTEND_HANDOFF.md`

### 22.10 Reentrada de Codex CLI

Cuando Codex CLI vuelva a trabajar después de una sesión de OpenCode/DeepSeek, debe leer primero:

- `AGENTS.md`
- `docs/ai-handoff/ACTIVE_CONTEXT.md`
- `docs/ai-handoff/CHANGELOG_AI.md`
- `docs/ai-handoff/CODEX_REENTRY.md`

Luego debe ejecutar:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git diff --stat
git diff --check
```

Codex CLI debe revisar los cambios realizados por DeepSeek antes de continuar.

Codex CLI debe decidir:

- si el cambio está dentro del alcance
- si requiere tests adicionales
- si requiere build frontend
- si requiere separación de commits
- si puede avanzar a commit
- si puede abrir Pull Request