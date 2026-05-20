# BACKEND_HANDOFF — Always Beautiful

## Responsable backend auxiliar actual

DeepSeek V4 Flash vía OpenCode.

## Revisor principal

Codex CLI.

## Rama actual

`feature/assistant-booking-conversion-flow`

## Alcance backend actual

- Assistant backend.
- Assistant-to-booking support.
- Booking/catalog/cart/orders contracts.
- pytest validation.
- curl validation.
- Revisión de rutas, schemas, services y tools.

## Módulos backend relevantes

- `services/api/app/assistant/*`
- `services/api/app/assistant/tools/*`
- `services/api/app/booking/*`
- `services/api/app/catalog/*`
- `services/api/app/cart/*`
- `services/api/app/orders/*`
- `services/api/tests/assistant/*`

## Diagnóstico backend inicial — DeepSeek V4 Flash

DeepSeek V4 Flash realizó un diagnóstico en Plan Mode sobre el soporte backend del flujo assistant-to-booking conversion.

### Hallazgos principales

- Existe endpoint conversacional del assistant.
- Existen schemas específicos del assistant.
- Existen tools del assistant para booking, cart, catalog, professional, availability y payment.
- Existen módulos backend separados para booking, catalog, cart y orders.
- Existen tests específicos del assistant.
- El assistant todavía no crea booking real.
- El assistant todavía no crea order real.
- El assistant genera `cart_payload`, pero no lo convierte directamente en carrito real.
- La disponibilidad sigue siendo tentativa o mock.
- El assistant depende parcialmente de datos estáticos para servicios/profesionales.
- No existe sincronización fuerte con catálogo real.

### Contratos existentes

- Assistant conversa mediante `/assistant/chat`.
- Assistant puede entregar quick replies.
- Assistant puede entregar `cart_payload`.
- Assistant puede guiar al usuario hacia booking/cart.
- Booking, catalog, cart y orders existen como módulos separados.

### Contratos débiles o faltantes

- No existe contrato backend formal assistant → cart.
- No existe mapping robusto service label → catalog item UUID.
- No existe contrato assistant → booking real.
- No existe contrato assistant → orders.
- No existe persistencia real de sesión assistant.
- No existe disponibilidad real conectada al módulo booking.

## Riesgos backend actuales

- Desincronización entre assistant y catálogo real.
- `cart_payload` interpretado manualmente por frontend.
- Disponibilidad mock.
- Sesión en memoria.
- Booking real requiere datos de clienta que todavía no se recolectan.
- Posible crecimiento excesivo de alcance si se intenta conectar booking, cart, orders y payments en una sola intervención.

## Validación backend recomendada

Ejecutar desde la raíz del repositorio:

```bash
cd services/api
source .venv/bin/activate
pytest tests/assistant/test_assistant_routes.py -v
deactivate
cd ../..
git status --short
## Backend handoff update — Cart booking deposit draft

### Current backend milestone
The cart domain now exposes the first formal backend contract for assistant-to-cart booking deposit conversion:

POST /cart/booking-deposit/draft

### Purpose
Move booking deposit draft responsibility from frontend/sessionStorage toward the backend cart domain.

### Domain boundary
- assistant guides commercial intent
- cart creates the draft
- booking will confirm the real booking later
- payments will execute real payment later
- orders will provide commercial traceability later

### Current implementation
Implemented:
- BookingDepositDraftCreate
- BookingDepositDraftItemResponse
- BookingDepositDraftResponse
- CartService.create_booking_deposit_draft
- POST /cart/booking-deposit/draft
- API tests for draft creation, pending price, deterministic draft id and invalid payload

### Explicit non-goals
This stage does not:
- persist a draft in database
- create a booking
- create an order
- execute payment
- consume catalog IDs
- modify frontend
- modify assistant

### Validated behavior
The endpoint was smoke-tested through curl and returned HTTP 201 Created with:
- type=booking_deposit_draft
- status=draft
- deposit_percentage=20
- payment_status=not_executed
- booking_status=not_created
- order_status=not_created

### Backend risks to review
1. Determine whether the endpoint must support multiple services through items[] before frontend integration.
2. Decide whether uuid5 deterministic draft_id is acceptable for this stage.
3. Evaluate whether service_price float should remain temporarily or move toward amount/currency.
4. Consider future fields:
   - assistant_session_id
   - client_session_id
   - expires_at
   - currency
   - catalog_item_id
   - professional_id as stable backend identifier

### Recommended next backend review
DeepSeek V4 Flash should review the new cart contract before frontend migration.
