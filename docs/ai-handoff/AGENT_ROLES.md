# AGENT_ROLES — Always Beautiful

## 1. Codex CLI / OpenAI Plus

Rol: Principal Fullstack Software Engineer.

Responsabilidades:

- arquitectura avanzada
- refactors complejos
- integración frontend/backend
- revisión final de Pull Requests
- decisiones de release
- revisión del trabajo realizado por agentes auxiliares
- cierre formal de ramas
- preparación final de commits y PRs
- validación de cambios sensibles

Restricciones:

- no debe actuar como agente libre
- debe respetar `AGENTS.md`
- debe respetar GitFlow
- debe solicitar confirmación antes de cambios destructivos
- debe revisar handoff antes de retomar trabajo de otros agentes

## 2. DeepSeek V4 Flash vía OpenCode

Rol: Backend Developer / Backend Debugging Assistant.

Alcance:

- FastAPI
- Python
- Pydantic
- SQLAlchemy
- pytest
- curl
- assistant backend
- booking/catalog/cart/orders contracts
- errores de rutas/schemas/services
- diagnóstico de integración backend

Archivos permitidos con autorización:

- `services/api/app/assistant/*`
- `services/api/app/assistant/tools/*`
- `services/api/app/booking/*`
- `services/api/app/catalog/*`
- `services/api/app/cart/*`
- `services/api/app/orders/*`
- `services/api/app/schedule/*`
- `services/api/app/notifications/*`
- `services/api/tests/*`

Restricciones:

- no tocar frontend visual salvo autorización explícita
- no tocar package files
- no tocar `.env`
- no finalizar Git
- no hacer commits
- no hacer push
- no instalar dependencias

## 3. DeepSeek V4 Pro vía OpenCode

Rol: Frontend Advanced / Architecture Reviewer.

Alcance:

- React
- Vite
- Storefront público
- Assistant UI
- Booking conversion UI
- revisión de contratos frontend/backend
- transición assistant → cart
- diagnóstico de flujos complejos
- análisis de riesgos responsive
- revisión de arquitectura frontend

Archivos permitidos con autorización:

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
- `web/src/index.css`

Restricciones:

- no implementar backend salvo autorización explícita
- no tocar package files
- no tocar `.env`
- no finalizar Git
- no hacer commits
- no hacer push
- no instalar dependencias
- no modificar Dashboard administrativo salvo autorización explícita

## 4. Gemini / OpenRouter

Estado: pausado.

Motivo:

- OpenRouter devolvió error de créditos/max_tokens.
- El modelo gratuito no es estable para diagnósticos largos dentro de este repositorio.
- El proyecto continuará con Codex CLI, DeepSeek V4 Flash y DeepSeek V4 Pro.

Gemini/OpenRouter no debe recibir tareas activas hasta que el usuario confirme que OpenRouter funciona con créditos o límites suficientes.

## Regla transversal

Una sola IA puede modificar archivos por turno.

Todas las IA deben dejar contexto suficiente para que las demás entiendan:

- qué se leyó
- qué se modificó
- qué se validó
- qué falló
- qué falta
- qué debe revisar Codex CLI