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

## Actualización de contexto activo — 2026-05-19

### Rama actual
feature/assistant-booking-conversion-flow

### Último contrato backend implementado
POST /cart/booking-deposit/draft

### Responsable de implementación
Codex CLI

### Estado local actual
La implementación backend del draft de carrito fue creada y validada localmente.

### Validación completada
- Tests del draft de carrito: 4 passed
- Tests del assistant: 43 passed
- git diff --check: limpio
- Prueba curl de humo: HTTP 201 Created

### Próximo plan de commits
1. feat(cart): crear draft backend de abono de reserva
2. docs(ai): registrar contrato cart draft y validaciones

### Actualización del protocolo de validación
Los próximos prompts de implementación para Codex deben incluir:
- Comandos pytest relevantes al dominio modificado
- Build de npm cuando el frontend o la salud general de la rama lo requiera
- Pruebas curl de humo para endpoints nuevos o modificados
- git diff --check
- git status --short

### Próxima revisión IA
DeepSeek V4 Flash debe revisar la calidad del contrato backend antes de cualquier migración frontend.

### No hacer todavía
- No mergear hacia develop
- No cerrar la rama feature
- No migrar frontend todavía
- No implementar pago real
- No crear booking real
- No crear order real

## Bitácora de Coordinación IA — Revisión backend de DeepSeek V4 Flash después del Cart Draft Stage 1A

### Rama actual
feature/assistant-booking-conversion-flow

### Estado del working tree antes del Stage 1B
Los cambios recuperados del chat assistant fueron movidos a stash para mantener el working tree limpio antes de implementar el siguiente ajuste exclusivamente backend.

Stash actual:
- stash@{0}: pausa del assistant chat: cambios recuperados antes de la fase 1b del contrato del carrito

### Resultado de la revisión backend
DeepSeek V4 Flash revisó el contrato Cart Draft Stage 1A y confirmó:
- POST /cart/booking-deposit/draft pertenece al dominio cart.
- El endpoint evita correctamente crear booking, order o payment.
- El contrato actual es una primera base backend válida.

### Hallazgos bloqueantes antes de migrar frontend
DeepSeek V4 Flash identificó que Stage 1A no debe ser consumido por frontend todavía porque:
1. El endpoint no soporta drafts multi-servicio mediante items[].
2. draft_id no incluye assistant_session_id ni client_session_id.
3. payment_status difiere entre el lenguaje del payload del assistant y la respuesta backend del cart.
4. El request no incluye assistant_session_id para correlacionar el draft con la sesión del assistant.

### Decisión
Avanzar con Cart Draft Stage 1B antes de volver a la implementación frontend o al flujo del chat assistant.

### Próximo responsable de implementación
Codex CLI

### Alcance de implementación del Stage 1B
Permitido:
- services/api/app/cart/schemas.py
- services/api/app/cart/service.py
- services/api/app/cart/routes.py
- services/api/tests/cart/test_booking_deposit_draft.py

No permitido:
- services/api/app/assistant/*
- web/*
- services/api/app/orders/*
- services/api/app/payments/*
- services/api/app/booking/*
- services/api/app/catalog/*

### Próximos requisitos de validación
Codex CLI debe ejecutar:
- PYTHONPATH=services/api services/api/.venv/bin/pytest services/api/tests/cart/test_booking_deposit_draft.py -v
- PYTHONPATH=services/api services/api/.venv/bin/pytest services/api/tests/assistant/test_assistant_routes.py -v
- Prueba curl de humo para draft multi-servicio
- Prueba curl de humo para comprobar que un assistant_session_id distinto produce un draft_id distinto
- git diff --check
- git status --short

## Bitácora de Coordinación IA — Implementación Codex Cart Draft Stage 1B pendiente de revisión backend

### Rama actual
feature/assistant-booking-conversion-flow

### Estado actual de la implementación
Codex CLI implementó Cart Draft Stage 1B localmente. La implementación todavía no está commiteada ni subida al remoto.

### Archivos modificados pendientes de revisión
- services/api/app/cart/schemas.py
- services/api/app/cart/service.py
- services/api/tests/cart/test_booking_deposit_draft.py

### Comportamiento implementado en Stage 1B
- BookingDepositDraftCreate ahora soporta items[].
- BookingDepositDraftCreate ahora requiere assistant_session_id.
- source está restringido a Literal["assistant", "web", "admin"].
- El seed de draft_id ahora incluye assistant_session_id.
- cart_count se deriva desde len(items).
- Los campos top-level de Stage 1A se mantienen temporalmente por compatibilidad.
- No se modificaron archivos del assistant.
- No se modificaron archivos del frontend.
- Codex no modificó documentación.
- El stash del chat assistant sigue pausado.

### Validación reportada por Codex
- Tests del draft de carrito: 6 passed.
- Tests de regresión del assistant en estado limpio de rama: 22 passed.
- Curl de draft multi-servicio: HTTP 201.
- Curl con el mismo assistant_session_id: mismo draft_id.
- Curl con distinto assistant_session_id: distinto draft_id.
- Curl con source inválido: HTTP 422.
- git diff --check: limpio.

### Revisión pendiente
DeepSeek V4 Flash debe revisar el contrato backend Stage 1B antes de hacer commit y push.

### Restricciones importantes
- No recuperar todavía el stash del chat assistant.
- No commitear Stage 1B antes de la revisión backend.
- No subir Stage 1B al remoto antes de la revisión backend.
- No migrar frontend todavía.
## Bitácora de Coordinación IA — Aprobación backend de Cart Draft Stage 1B

### Rama actual
feature/assistant-booking-conversion-flow

### Resultado de revisión
DeepSeek V4 Flash revisó la implementación local de Cart Draft Stage 1B realizada por Codex CLI y aprobó la etapa para commit.

### Estado de Stage 1B
Cart Draft Stage 1B queda aprobado como contrato backend estable para continuar hacia revisión frontend.

### Comportamiento backend aprobado
- BookingDepositDraftCreate soporta items[].
- BookingDepositDraftCreate requiere assistant_session_id.
- source está restringido a Literal["assistant", "web", "admin"].
- draft_id incluye assistant_session_id en el seed.
- cart_count se deriva desde len(items).
- Se mantiene compatibilidad temporal con los campos top-level de Stage 1A.
- El endpoint conserva estados no finales:
  - status=draft
  - confirmation_status=not_confirmed
  - payment_status=not_executed
  - booking_status=not_created
  - order_status=not_created

### Validaciones reportadas
- Tests cart: 6 passed.
- Tests assistant base: 22 passed.
- Curl multi-servicio: HTTP 201.
- Curl mismo assistant_session_id: mismo draft_id.
- Curl distinto assistant_session_id: distinto draft_id.
- Curl source inválido: HTTP 422.
- git diff --check: limpio.

### Decisión
Guardar Stage 1B en commit local, actualizar la Bitácora IA en commit local y mantener la rama sin push hasta que el flujo assistant → cart quede validado. Luego recuperar el stash del assistant chat para iniciar revisión frontend con DeepSeek V4 Pro.

### Stash del chat assistant
Los 15 archivos del assistant chat siguen pausados en stash y no deben recuperarse hasta que Stage 1B esté protegido al menos en commits locales coherentes.

### Próximo modelo
DeepSeek V4 Pro debe revisar la integración frontend después de recuperar el stash.
