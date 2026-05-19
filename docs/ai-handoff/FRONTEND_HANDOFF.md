# FRONTEND_HANDOFF — Always Beautiful

## Responsable frontend avanzado auxiliar actual

DeepSeek V4 Pro vía OpenCode.

## Revisor principal

Codex CLI.

## Rama actual

`feature/assistant-booking-conversion-flow`

## Alcance frontend actual

- Storefront público.
- Assistant booking conversion flow.
- React/Vite/CSS.
- Assistant UI.
- Booking/cart transition.
- Contrato frontend/backend.
- Interpretación actual de `cart_payload`.
- Futura transición hacia contrato formal del dominio `cart`.

## Módulos frontend relevantes

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

## No tocar sin autorización

- admin layout
- backend
- package files
- `.env`
- routing global salvo aprobación explícita
- `package.json`
- `package-lock.json`
- cambios globales de diseño no autorizados
- Dashboard administrativo

## Estado frontend actual

DeepSeek V4 Pro realizó diagnóstico frontend avanzado en Plan Mode.

No modificó archivos.

No ejecutó build.

## Estado backend relacionado

DeepSeek V4 Flash diagnosticó backend en Plan Mode.

El usuario ejecutó:

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

## Hallazgos frontend principales

- `AssistantChatWidget.jsx` es el orquestador principal del chat.
- `AssistantMessageList.jsx` renderiza mensajes y quick replies.
- `assistantClient.js` conecta con `/assistant/chat`.
- `CartPage.jsx` lee el handoff desde `sessionStorage`.
- `cart_payload` se interpreta manualmente en frontend.
- `isCompleteCartPayload` contiene reglas de negocio hardcodeadas.
- El handoff actual no crea una entidad real de carrito en backend.
- Si `cart_handoff` falla, puede no existir feedback visual suficiente.
- El session ID usa `localStorage`, lo que puede mezclar sesiones entre pestañas.
- `index.css` mezcla estilos Dashboard, Storefront y Assistant, por lo que cualquier cambio visual debe ser mínimo y validado.

## Concordancia con backend

El diagnóstico frontend coincide con el diagnóstico backend:

- Backend entrega `cart_payload`.
- Frontend interpreta `cart_payload`.
- Cart todavía no tiene contrato formal para convertir ese payload en carrito real.
- El punto débil principal es la frontera assistant/cart.

## Decisión de arquitectura preferida

La solución profesional preferida es que el dominio `cart` exponga un contrato formal, por ejemplo:

- `POST /cart/booking-deposit/draft`

Este endpoint debería recibir un payload normalizado del assistant y devolver una entidad/draft de carrito controlada por backend.

El frontend debería dejar de gobernar reglas comerciales como porcentaje de abono, estados de pago o validación profunda del payload.

## Validaciones frontend recomendadas

Cuando Codex autorice validación frontend, ejecutar:

```bash
npm --prefix web run build
git diff --check
git status --short
```

## Próximo paso recomendado

Pasar a Codex CLI en modo diagnóstico/arquitectura para decidir:

- si se crea `POST /cart/booking-deposit/draft`
- qué archivos backend y frontend se tocarán
- qué tests se deben agregar
- si el primer cambio lo ejecuta Codex directamente o DeepSeek bajo instrucciones
- cómo separar commits backend/frontend