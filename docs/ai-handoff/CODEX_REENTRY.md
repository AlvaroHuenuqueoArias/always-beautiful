# CODEX_REENTRY — Always Beautiful

## Propósito

Este archivo prepara a Codex CLI para retomar trabajo después de sesiones realizadas por DeepSeek.

Codex CLI mantiene la autoridad técnica final del proyecto.

## Rama actual

`feature/assistant-booking-conversion-flow`

## Agentes auxiliares activos

- DeepSeek V4 Flash vía OpenCode.
- DeepSeek V4 Pro vía OpenCode.

## Agente pausado

- Gemini 3 Flash Preview vía OpenCode + OpenRouter queda pausado por error de créditos/max_tokens.

## Últimos agentes auxiliares usados

- DeepSeek V4 Flash vía OpenCode.

## Resumen del trabajo auxiliar

DeepSeek V4 Flash realizó diagnóstico backend del flujo assistant-to-booking conversion.

Hallazgos principales:

- Assistant conversa y entrega payloads.
- Assistant no crea booking real.
- Assistant no crea order real.
- Assistant no convierte `cart_payload` en carrito real.
- Disponibilidad sigue siendo tentativa/mock.
- Catálogo/profesionales siguen parcialmente hardcodeados.
- Falta contrato robusto assistant → cart.

## Validaciones completadas

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

## Archivos cambiados por agentes auxiliares

Pendiente de confirmar.

Durante el diagnóstico de DeepSeek V4 Flash no se modificaron archivos.

## Fallos

OpenRouter/Gemini no pudo ejecutar diagnóstico por error de créditos/max_tokens.

## Riesgos para Codex

- Existe `cart_payload`, pero todavía no hay contrato formal assistant/cart.
- La solución profesional parece ser un endpoint del dominio `cart`, no del dominio `assistant`.
- El frontend todavía debe ser diagnosticado por DeepSeek V4 Pro.
- Hay cambios pendientes en backend, frontend, `AGENTS.md` y `docs/ai-handoff/`.
- No debe hacerse commit antes de revisar el diagnóstico frontend.
- No deben ejecutarse curl’s manuales todavía.

## Primera tarea para Codex al reentrar

Leer:

- `AGENTS.md`
- `docs/ai-handoff/ACTIVE_CONTEXT.md`
- `docs/ai-handoff/CHANGELOG_AI.md`
- `docs/ai-handoff/CODEX_REENTRY.md`

Luego ejecutar:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git diff --stat
git diff --check
```

## Criterios para que Codex retome

Codex debe retomar cuando:

- haya cambios complejos de arquitectura
- haya integración frontend/backend sensible
- DeepSeek V4 Flash o DeepSeek V4 Pro detecten riesgos fuera de su alcance
- se requiera commit formal
- se requiera Pull Request
- se requiera merge
- se requiera decisión de alcance
- se detecte riesgo sobre una base estable
## Codex re-entry update — Cart draft contract implemented

### Current status
Codex implemented the first backend cart contract:

POST /cart/booking-deposit/draft

### Do not repeat
Do not recreate the same endpoint.
Do not move the endpoint to assistant.
Do not touch frontend until instructed.
Do not create booking, order or payment from this endpoint.

### If re-entering backend
First inspect:
- services/api/app/cart/schemas.py
- services/api/app/cart/service.py
- services/api/app/cart/routes.py
- services/api/tests/cart/test_booking_deposit_draft.py

### Next likely backend task
If backend review approves, evolve the contract only if required to support multi-service cart drafts.

Potential future direction:
- replace single service fields with items[]
- add amount/currency fields
- add session identifiers
- keep compatibility with current assistant payloads if possible

### Required checks before any future backend commit
- PYTHONPATH=services/api services/api/.venv/bin/pytest services/api/tests/cart/test_booking_deposit_draft.py -v
- PYTHONPATH=services/api services/api/.venv/bin/pytest services/api/tests/assistant/test_assistant_routes.py -v
- npm --prefix web run build when frontend or branch health requires it
- curl smoke tests for new or changed HTTP endpoints
- git diff --check
