# ACTIVE_CONTEXT — Always Beautiful

## Rama actual

`feature/assistant-booking-conversion-flow`

## Objetivo actual

Construir y validar el flujo `assistant-to-booking conversion` sin romper Storefront, Admin Dashboard ni módulos backend estables.

## Estado base conocido

El proyecto ya incluye:

- backend modular con FastAPI
- módulo `assistant`
- tools del assistant
- tests del assistant
- cliente frontend para assistant
- componentes frontend del chat
- widget flotante
- quick replies iniciales
- handoff seguro hacia carrito
- módulos separados de booking, catalog, cart y orders
- carpeta `docs/ai-handoff/` creada para coordinación multiagente

## Orquestación IA actual

### IA principales

- Codex CLI / OpenAI Plus — principal fullstack.
- DeepSeek V4 Flash vía OpenCode — backend/debugging.
- DeepSeek V4 Pro vía OpenCode — frontend avanzado/arquitectura.

### IA pausada

- Gemini 3 Flash Preview vía OpenCode + OpenRouter — pausada por error de créditos/max_tokens en OpenRouter.

## Última intervención registrada

DeepSeek V4 Flash realizó diagnóstico backend en Plan Mode.

## Última validación ejecutada

El usuario ejecutó manualmente:

```bash
cd services/api
source .venv/bin/activate
pytest tests/assistant/test_assistant_routes.py -v
deactivate
cd ../..
git status --short
```

Resultado:

```text
43 tests passed in 16.21s
```

## Última IA que modificó archivos

Ninguna durante el diagnóstico de DeepSeek V4 Flash.

## Últimos archivos modificados por IA

Ninguno durante el diagnóstico de DeepSeek V4 Flash.

## Estado Git conocido

Hay cambios pendientes en:

- `AGENTS.md`
- `services/api/app/assistant/graph.py`
- `services/api/app/assistant/policies.py`
- `services/api/app/assistant/schemas.py`
- `services/api/app/assistant/service.py`
- `services/api/app/assistant/tools/booking_tools.py`
- `services/api/app/assistant/tools/cart_tools.py`
- `services/api/app/assistant/tools/professional_tools.py`
- `services/api/tests/assistant/test_assistant_routes.py`
- `web/src/components/shared/AssistantChatWidget.jsx`
- `web/src/components/shared/AssistantMessageList.jsx`
- `web/src/components/shared/PublicHeader.jsx`
- `web/src/index.css`
- `web/src/layouts/PublicLayout.jsx`
- `web/src/pages/public/CartPage.jsx`
- `web/src/services/assistantClient.js`
- `docs/ai-handoff/`

## Hallazgos backend principales

- Assistant conversa y entrega payloads.
- Assistant no crea booking real.
- Assistant no crea order real.
- Assistant no convierte `cart_payload` en carrito real.
- Disponibilidad sigue siendo tentativa/mock.
- Catálogo/profesionales siguen parcialmente hardcodeados.
- Falta contrato robusto assistant → cart.
- La suite actual de tests del assistant pasa correctamente.

## Decisión de arquitectura preferida

La solución profesional preferida para el puente assistant → cart es que el dominio `cart` exponga un contrato formal, por ejemplo:

- `/cart/booking-deposit`
- `/cart/booking-deposit/draft`

La opción `/assistant/cart/handoff` queda descartada como diseño definitivo y solo podría considerarse como adaptador temporal si Codex CLI lo aprueba.

## Riesgos actuales

- Desalineación frontend/backend.
- Regresión visual del Storefront.
- Inconsistencia del flujo assistant.
- Desajuste de rutas/schemas backend.
- `cart_payload` interpretado manualmente por frontend.
- Consumo excesivo de créditos DeepSeek si se usa V4 Pro sin necesidad.
- Reentrada de Codex sin contexto actualizado.
- Implementar un endpoint en el dominio equivocado y generar deuda técnica.
- Mantener referencias a Gemini/OpenRouter en documentos operativos cuando OpenRouter no está disponible.

## Acciones prohibidas

- `git add`
- `git commit`
- `git push`
- `git merge`
- `git reset --hard`
- `git clean`
- editar archivos `.env`
- instalar dependencias
- refactors amplios sin autorización
- autorizar Build Mode antes de diagnóstico frontend
- ejecutar curl’s manuales sin instrucción explícita
- usar OpenRouter/Gemini como requisito para avanzar

## Próxima acción recomendada

1. Actualizar `AGENTS.md` y archivos `docs/ai-handoff/` para dejar solo tres IA operativas.
2. Ejecutar diagnóstico frontend con DeepSeek V4 Pro en Plan Mode.
3. Copiar el diagnóstico completo en ChatGPT.
4. Comparar diagnóstico frontend con diagnóstico backend.
5. No autorizar Build Mode hasta completar revisión multiagente.
## Active context update — 2026-05-19

### Current branch
feature/assistant-booking-conversion-flow

### Latest implemented backend contract
POST /cart/booking-deposit/draft

### Implementation owner
Codex CLI

### Current local status
The cart draft backend implementation has been created and validated locally.

### Validation completed
- cart draft tests: 4 passed
- assistant tests: 43 passed
- git diff --check: clean
- curl smoke test: HTTP 201 Created

### Next commit plan
1. feat(cart): crear draft backend de abono de reserva
2. docs(ai): registrar contrato cart draft y validaciones

### Validation protocol update
Future Codex implementation prompts must include:
- pytest commands relevant to the changed domain
- npm build when frontend or branch health requires it
- curl smoke tests for new or changed HTTP endpoints
- git diff --check
- git status --short

### Next AI review
DeepSeek V4 Flash should review backend contract quality before any frontend migration.

### Do not do yet
- do not merge to develop
- do not close the feature branch
- do not migrate frontend yet
- do not implement real payment
- do not create real booking
- do not create real order
