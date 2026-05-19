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