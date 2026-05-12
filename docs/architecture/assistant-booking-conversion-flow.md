# Assistant Booking Conversion Flow

## 1. Executive Summary

Este documento define la arquitectura funcional y comercial para evolucionar el chat assistant del Storefront hacia un flujo guiado de conversion de reservas. El objetivo no es confirmar reservas reales en esta rama, sino establecer reglas, contratos y criterios de validacion para que futuras Pull Requests implementen el flujo de manera incremental, auditable y segura.

El flujo propuesto conecta conversacion, seleccion de servicio, profesional, dia, hora, disponibilidad read-only, abono del 20%, handoff a carrito/checkout y estrategia de notificaciones. La primera implementacion debe mantener estado comercial tentativo hasta que exista pago validado y confirmacion operativa.

## 2. Business Objective

El negocio necesita que una clienta pueda pasar desde una conversacion natural hacia una reserva comercial tentativa, sin romper las reglas de pago ni prometer disponibilidad real antes de validarla.

Objetivos comerciales:

- Guiar a la clienta paso a paso desde intencion de reserva hasta pre-reserva.
- Reducir friccion al elegir servicio, profesional, fecha y hora.
- Validar compatibilidad profesional/servicio antes de ofrecer continuidad.
- Solicitar abono obligatorio del 20% para confirmar servicios.
- Preparar redireccion futura a `/cart` o `/checkout`.
- Informar que el comprobante se enviara por correo y WhatsApp, con SMS como fallback futuro si la clienta no usa WhatsApp.
- Evitar frases de confirmacion antes del pago validado.

## 3. Scope

Alcance de esta rama y de este documento:

- Reglas comerciales para `booking_conversion`.
- Contrato JSON propuesto para respuestas del assistant.
- Flujo conversacional objetivo.
- State machine funcional.
- Politicas de servicio, profesional, disponibilidad y abono.
- Handoff propuesto hacia carrito/checkout.
- Estrategia documental de notificaciones.
- Roadmap tecnico por PRs.
- Criterios de aceptacion y validacion por build, pytest y curls.

## 4. Out of Scope

Fuera de alcance para este PR 1:

- Crear reservas reales.
- Bloquear slots reales.
- Integrar pagos reales, Mercado Pago, PayPal o proveedor productivo.
- Enviar correos, WhatsApp o SMS reales.
- Activar LLM real.
- Activar LangGraph productivo.
- Modificar logica productiva backend.
- Modificar frontend funcional.
- Persistir estado conversacional definitivo en base de datos.
- Confirmar precios, disponibilidad o agenda real sin datos del salon.

## 5. Impacted Modules

Modulos impactados por la arquitectura futura:

- Modulo 6 - Notifications: comprobante, email, WhatsApp preferente y SMS fallback futuro.
- Modulo 7 - Booking Engine: pre-reserva, seleccion de servicio/profesional y futura reserva definitiva.
- Modulo 8 - Schedule Engine: disponibilidad, pausas, bloqueos y horario laboral.
- Modulo 10 - Cart + Checkout: payload de abono, estado `pending_deposit` y redireccion controlada.
- Modulo 13 - Storefront Experience: chat, quick replies, rutas publicas y experiencia mobile.
- Modulo 14 - Recommendation + Assistant Intelligence Layer: estado conversacional, politicas, clasificacion de intencion y contratos.
- Modulo 4 - Payments Core: dependencia futura para validar pago, sin integracion real en esta ejecucion.

## 6. Current Architecture Baseline

### Assistant

Existe `services/api/app/assistant/` con:

- `routes.py`: expone `GET /assistant/health` y `POST /assistant/chat`.
- `schemas.py`: define `AssistantChatRequest` y `AssistantChatResponse`.
- `service.py`: orquesta memoria local y `AssistantGraphRunner`.
- `state.py`: define `AssistantIntent`, `AssistantChannel` y `AssistantState`.
- `policies.py`: contiene politica de abono del 20% y deteccion de intentos de evitar abono.
- `graph.py`: clasifica intencion por palabras clave y resuelve nodos de booking, producto o general.
- `tools/booking_tools.py`: genera orientacion de reserva sin confirmar disponibilidad real.
- `tools/cart_tools.py`: entrega acciones futuras de carrito.
- `tools/payment_tools.py`: expone politica simulada de abono.
- `tools/professional_tools.py`: mantiene profesionales mock por rol/cobertura.

Estado actual: funcional y deterministico. Todavia no soporta `flow_step`, quick replies estructurados, seleccion incremental, disponibilidad detallada ni payload de carrito.

### Booking

Existe `services/api/app/booking/` con rutas, schemas, repository y service. El modulo permite crear reservas con estado `BOOKED`, listar, cancelar, consultar disponibilidad diaria y generar slots disponibles por profesional, fecha y duracion.

Riesgo actual: el flujo conversacional no debe llamar creacion de booking real mientras el estado comercial sea tentativo. Para assistant se requiere primero una capa `booking_draft` o `pending_deposit`.

### Schedule

Existe `services/api/app/schedule/` con template semanal, pausas, bloqueos por fecha y consulta de agenda diaria. Esta base puede alimentar disponibilidad read-only futura.

Pendiente: datos reales del salon, horarios por profesional, pausas definitivas, feriados, excepciones y duraciones reales por servicio.

### Cart + Checkout

Existe `services/api/app/cart/` con creacion de carrito, agregacion de items de catalogo, validacion de stock y regla de cantidad para servicios. En frontend existen shells publicos para `CartPage.jsx` y `CheckoutPage.jsx`.

Pendiente: item de abono de reserva, saldo restante, estado `pending_deposit`, payload mixto servicio/producto y redireccion controlada desde el assistant.

### Notifications

Existe `services/api/app/notifications/` con schemas, service, repository y dispatchers base de email/webhook. Todavia no hay envio real de WhatsApp ni SMS.

Pendiente: contrato de evento, plantillas, preferencia de canal, proveedor, costos de SMS y disparo post-pago.

### Storefront Chat

Existe chat assistant en `web/src/components/shared/`:

- `FloatingAssistantButton.jsx`
- `AssistantChatWidget.jsx`
- `AssistantChatPanel.jsx`
- `AssistantMessageList.jsx`
- `AssistantComposer.jsx`

El chat recibe respuestas del backend desde `web/src/services/assistantClient.js`, muestra mensajes, aviso de deposito y sanitiza frases no permitidas como "reserva confirmada", "hora confirmada" y "cita agendada".

## 7. Proposed Conversation Flow

Flujo objetivo:

1. La clienta expresa una intencion de reserva.
2. El assistant entra a `booking_conversion`.
3. Si el servicio no esta claro, pregunta que servicio desea.
4. El assistant clasifica servicio como `styling`, `cosmetology`, `treatment`, `product` o `unknown`.
5. El assistant solicita o valida profesional.
6. El sistema valida compatibilidad servicio/profesional.
7. El assistant solicita fecha si falta.
8. Si la clienta indica solo dia, por ejemplo "miércoles", responde: "Perfecto. ¿A que hora prefieres agendar el miércoles?"
9. Si la clienta indica hora, valida disponibilidad read-only.
10. Si el horario esta disponible, ofrece continuar con abono del 20%.
11. Si la clienta acepta, prepara payload para `/cart` o `/checkout`.
12. El estado permanece `pending_deposit` hasta pago validado.
13. Solo despues de pago validado una integracion futura podra crear reserva definitiva y disparar comprobante.

## 8. State Machine

Estados propuestos:

- `service_selection`: falta servicio o categoria.
- `professional_selection`: falta profesional o se debe resolver compatibilidad.
- `date_selection`: falta fecha.
- `time_selection`: falta hora.
- `availability_check`: el sistema revisa disponibilidad read-only.
- `deposit_confirmation`: el horario esta disponible y se solicita aceptar pago del 20%.
- `checkout_redirect`: se prepara handoff a `/cart` o `/checkout`.
- `product_selection`: flujo de recomendacion o compra de productos.
- `completed`: cierre conversacional no necesariamente equivalente a reserva confirmada.

Transiciones principales:

- `general` -> `booking_conversion` cuando hay intencion de agenda/reserva.
- `booking_conversion` -> `service_selection` si falta servicio.
- `service_selection` -> `professional_selection` si el servicio esta claro.
- `professional_selection` -> `date_selection` si profesional es compatible.
- `professional_selection` -> `service_selection` si la combinacion es incompatible y la clienta decide cambiar servicio.
- `date_selection` -> `time_selection` si falta hora.
- `time_selection` -> `availability_check` cuando existen servicio, profesional, fecha y hora.
- `availability_check` -> `deposit_confirmation` si el slot esta disponible.
- `availability_check` -> `time_selection` si el slot no esta disponible.
- `deposit_confirmation` -> `checkout_redirect` si la clienta acepta pagar 20%.
- `deposit_confirmation` -> `completed` si la clienta no desea continuar.

## 9. Commercial Rules

### A. Intencion de reserva

Si la clienta dice "quiero agendar", "quiero reservar", "quiero una hora" o "quiero agenda el miércoles", el assistant debe entrar al flujo `booking_conversion`.

Reglas:

- No debe confirmar reserva sin pago.
- Debe guiar paso a paso.
- Debe pedir informacion faltante antes de consultar disponibilidad.

### B. Servicio

El assistant debe preguntar que servicio desea. Debe distinguir entre:

- Estilismo.
- Cosmetología.
- Tratamiento capilar.
- Producto.
- Otra consulta.

Si el servicio no esta claro, debe pedir aclaracion antes de avanzar.

### C. Profesional

Profesionales oficiales:

- Nadia Luisa.
- María Ignacia.

Reglas:

- Nadia Luisa puede realizar servicios de estilismo profesional segun catalogo del negocio.
- María Ignacia realiza cosmetología.
- María Ignacia tambien puede cubrir agenda de estilismo profesional si el negocio lo permite.
- Si la clienta elige cosmetología con Nadia Luisa, el sistema debe bloquear esa combinacion y explicar: "Nadia Luisa no realiza servicios de cosmetología. Para ese servicio puede atenderte María Ignacia."

Botones requeridos:

- "Continuar con María Ignacia"
- "Cambiar servicio"
- "Elegir otra profesional"

### D. Dia y hora

Si la clienta indica solo el dia, por ejemplo "miércoles", el assistant debe preguntar: "Perfecto. ¿A que hora prefieres agendar el miércoles?"

Si la clienta indica hora, el sistema debe validar disponibilidad con los datos disponibles.

### E. Disponibilidad

La validacion debe considerar:

- Servicio.
- Profesional.
- Fecha.
- Hora.
- Duracion.
- Bloqueos.
- Reservas existentes.
- Pausas.
- Horario laboral.

En esta primera rama puede ser read-only/mock. No debe crear reserva definitiva.

### F. Abono 20%

Toda reserva de servicio debe requerir 20% de abono desde la web.

Antes del pago, el estado debe ser `pending_deposit` o `booking_draft`.

Texto permitido:

"Ese horario está disponible. ¿Deseas continuar y pagar el abono del 20% para confirmar tu hora?"

Botones:

- "Sí, continuar y pagar 20%"
- "No por ahora, gracias"

### G. Carrito/checkout

Si la clienta acepta pagar, se debe preparar redireccion a `/cart` o `/checkout`.

El handoff debe llevar:

- Servicio.
- Profesional.
- Fecha.
- Hora.
- Precio total.
- Abono 20%.
- Saldo restante 80%.
- Estado `pending_deposit`.

CTA recomendado:

- "Pagar 20% ahora"

Texto minimalista:

"Te enviaremos el comprobante por correo y WhatsApp. El saldo restante se paga en el salon."

### H. Productos

Si la clienta desea comprar productos, el assistant debe recomendar y ofrecer:

- "Agregar al carrito"
- "Ver otro producto"
- "Consultar con una profesional"

Producto fisico debe pagarse completo, salvo que el negocio defina otra politica.

Servicio + producto puede combinar abono del servicio + pago completo del producto.

### I. Notificaciones

Canales:

- Email base.
- WhatsApp preferente.
- SMS fallback si la clienta no usa WhatsApp.

SMS tiene costo operativo por proveedor y no debe integrarse todavia. Esta rama no debe enviar mensajes reales.

### J. Seguridad comercial

No usar antes de pago validado:

- "reserva confirmada"
- "hora confirmada"
- "cita agendada"

Usar:

- "reserva pendiente de abono"
- "solicitud de reserva"
- "pre-reserva"
- "horario disponible pendiente de pago"

## 10. Professional Compatibility Rules

Reglas propuestas:

| Servicio | Nadia Luisa | María Ignacia | Estado |
|---|---:|---:|---|
| Estilismo profesional | Permitido | Permitido si el negocio lo permite | Requiere catalogo real |
| Tratamiento capilar | Permitido | Permitido si el negocio lo permite | Requiere duracion/precio real |
| Cosmetología | Bloqueado | Permitido | Regla comercial obligatoria |
| Producto | No aplica | No aplica | Debe ir a producto/carrito |
| Unknown | Requiere aclaracion | Requiere aclaracion | No consultar disponibilidad |

Cuando exista incompatibilidad:

- `availability_status` debe ser `incompatible_professional`.
- `is_available` no debe presentarse como `true`.
- `quick_replies` debe ofrecer alternativa segura.
- El mensaje debe explicar la regla sin culpar a la clienta.

## 11. Booking Availability Rules

La disponibilidad futura debe ser read-only hasta que el pago quede validado.

Datos requeridos para validar:

- `selected_service.id`
- `selected_professional.id`
- `selected_date`
- `selected_time`
- `duration_minutes`
- horario laboral del profesional
- pausas
- bloqueos
- reservas existentes

Resultado esperado:

- `available`: se puede ofrecer abono.
- `unavailable`: se deben ofrecer horarios alternativos.
- `needs_more_info`: falta informacion obligatoria.
- `incompatible_professional`: profesional no puede realizar el servicio.

No se debe crear una reserva en `services/api/app/booking/service.py` mientras el flujo este en `availability_check` o `deposit_confirmation`.

## 12. Deposit Policy 20%

Politica:

- Servicios requieren abono del 20%.
- Productos se pagan completos salvo definicion comercial distinta.
- El saldo restante del servicio es 80%.
- El estado anterior al pago debe ser `booking_draft` o `pending_deposit`.
- El pago validado es condicion necesaria para confirmar.

Campos minimos:

- `requires_deposit: true`
- `deposit_percentage: 20`
- `deposit_amount`
- `remaining_amount`
- `safety.booking_confirmed: false`
- `safety.payment_required_before_confirmation: true`

## 13. Cart and Checkout Handoff

El handoff a carrito/checkout debe ser controlado y no debe inventar datos.

Payload minimo:

- `type: booking_deposit`
- item de servicio
- profesional
- fecha
- hora
- precio total
- abono 20%
- saldo 80%
- estado `pending_deposit`

Rutas objetivo:

- `/cart`: revision previa de item y montos.
- `/checkout`: pago del abono si el payload ya esta completo.

La eleccion entre `/cart` y `/checkout` debe depender de madurez UX y validacion de payload. Para PRs iniciales se recomienda `/cart`.

## 14. Product Recommendation Flow

Si la intencion es producto:

- Mantener `intent: product_recommendation`.
- Ofrecer productos del catalogo o mock controlado.
- No exigir abono de servicio.
- Ofrecer "Agregar al carrito", "Ver otro producto" o "Consultar con una profesional".
- Si existe servicio + producto, calcular mezcla: abono 20% del servicio + pago completo del producto.

No se deben prometer resultados cosmeticos, medicos o cientificos sin fuentes confiables.

## 15. Notification Strategy

### Email

Email es el canal base para comprobante y resumen. Debe integrarse primero como contrato/evento antes de envio real.

### WhatsApp

WhatsApp es canal preferente para comunicacion comercial, pero no debe integrarse en esta rama. La futura integracion debe usar proveedor autorizado, variables de entorno y sandbox.

### SMS fallback

SMS queda como fallback si la clienta no usa WhatsApp. Tiene costo operativo por proveedor y debe evaluarse antes de habilitarlo.

### No real integration

Este flujo no envia notificaciones reales. Solo documenta contrato y eventos futuros:

- `booking.deposit.pending`
- `booking.deposit.paid`
- `booking.confirmation.requested`
- `booking.confirmation.sent`

## 16. Assistant Response Contract

Contrato JSON propuesto:

```json
{
  "session_id": "string",
  "intent": "booking_conversion | product_recommendation | general",
  "flow_step": "service_selection | professional_selection | date_selection | time_selection | availability_check | deposit_confirmation | checkout_redirect | product_selection | completed",
  "message": "string",
  "selected_service": {
    "id": "string",
    "name": "string",
    "category": "styling | cosmetology | treatment | product | unknown",
    "duration_minutes": 0,
    "price": 0
  },
  "selected_professional": {
    "id": "string",
    "name": "Nadia Luisa | María Ignacia",
    "role": "stylist | cosmetologist | hybrid"
  },
  "selected_date": "YYYY-MM-DD | null",
  "selected_time": "HH:mm | null",
  "is_available": true,
  "availability_status": "available | unavailable | needs_more_info | incompatible_professional",
  "requires_deposit": true,
  "deposit_percentage": 20,
  "deposit_amount": 0,
  "remaining_amount": 0,
  "quick_replies": [
    {
      "label": "string",
      "value": "string",
      "action": "select_service | select_professional | select_time | continue_to_deposit | decline | add_to_cart | change_option"
    }
  ],
  "next_actions": ["string"],
  "redirect_target": "/cart | /checkout | null",
  "cart_payload": {
    "type": "booking_deposit | product | mixed",
    "items": []
  },
  "notification_channels": {
    "email": true,
    "whatsapp": true,
    "sms_fallback": false
  },
  "safety": {
    "booking_confirmed": false,
    "payment_required_before_confirmation": true
  }
}
```

Compatibilidad con contrato actual:

- `AssistantChatResponse` actual ya soporta `session_id`, `intent`, `message`, `requires_deposit`, `deposit_percentage` y `next_actions`.
- Los campos nuevos deben agregarse incrementalmente en PR 2 o posteriores.
- El frontend debe tolerar campos ausentes durante la transicion.

## 17. Frontend Requirements

Requisitos futuros:

- Renderizar quick replies como botones accesibles.
- Mantener composer usable para texto libre.
- Mostrar estado de abono 20% con copy comercial seguro.
- Evitar confirmaciones antes de pago validado.
- Preparar redireccion controlada a `/cart` o `/checkout`.
- Mostrar monto total, abono y saldo restante cuando existan datos reales.
- Mantener panel responsive y scroll interno.
- No romper `/admin`.

Archivos probablemente impactados en PRs futuros:

- `web/src/components/shared/AssistantChatWidget.jsx`
- `web/src/components/shared/AssistantMessageList.jsx`
- `web/src/components/shared/AssistantComposer.jsx`
- `web/src/services/assistantClient.js`
- `web/src/pages/public/CartPage.jsx`
- `web/src/pages/public/CheckoutPage.jsx`
- `web/src/pages/public/BookingPage.jsx`

## 18. Backend Requirements

Requisitos futuros:

- Ampliar `AssistantIntent` con `booking_conversion`.
- Crear `flow_step` en estado y schema.
- Crear politicas deterministicas en `services/api/app/assistant/policies.py`.
- Crear state machine en `services/api/app/assistant/state.py`.
- Mantener disponibilidad read-only.
- No llamar `create_booking` hasta pago validado.
- Crear contrato de handoff a cart/checkout.
- Crear mocks de notificacion antes de proveedores reales.

Archivos probablemente impactados en PRs futuros:

- `services/api/app/assistant/state.py`
- `services/api/app/assistant/policies.py`
- `services/api/app/assistant/schemas.py`
- `services/api/app/assistant/service.py`
- `services/api/app/assistant/tools/booking_tools.py`
- `services/api/app/assistant/tools/professional_tools.py`
- `services/api/app/assistant/tools/cart_tools.py`
- `services/api/tests/assistant/test_assistant_routes.py`

## 19. Data Requirements from the Salon

Datos reales requeridos antes de activar flujo productivo:

- Lista final de servicios.
- Categorias oficiales.
- Duracion por servicio.
- Precio total por servicio.
- Servicios que realiza Nadia Luisa.
- Servicios que realiza María Ignacia.
- Confirmacion de si María Ignacia cubre estilismo profesional.
- Horarios laborales por profesional.
- Pausas.
- Bloqueos.
- Dias no laborales.
- Politica de reprogramacion/cancelacion.
- Texto comercial oficial para comprobantes.
- Canal preferente por clienta: email, WhatsApp o SMS fallback.
- Costo y proveedor SMS si se habilita.

## 20. Risks

Riesgos principales:

- Confirmar una reserva antes de pago validado.
- Crear reserva real desde el assistant sin handoff seguro.
- Ofrecer horarios sin considerar bloqueos o pausas.
- Permitir combinacion cosmetología + Nadia Luisa.
- Mezclar producto fisico con abono de servicio sin desglose.
- Prometer comprobante por WhatsApp/SMS sin integracion real.
- Romper el contrato actual del widget al agregar campos nuevos.
- Introducir dependencia de LLM o LangGraph productivo sin aprobacion.
- Conectar pagos reales sin sandbox ni variables seguras.

Mitigaciones:

- State machine deterministica.
- Safety flags obligatorios.
- Tests de frases prohibidas.
- Curls de booking/product/no-deposit.
- Disponibilidad read-only hasta pago validado.
- PRs pequenos y merge commits hacia `develop`.

## 21. Testing Strategy

Estrategia:

- Tests unitarios de politicas del assistant.
- Tests de compatibilidad profesional/servicio.
- Tests de estado `booking_conversion`.
- Tests de disponibilidad mock/read-only.
- Tests de rechazo de reserva sin abono.
- Tests de contrato JSON.
- Build frontend antes de commit.
- Curls minimos contra `/assistant/health` y `/assistant/chat`.

Casos minimos:

- "Quiero agendar el miércoles."
- "Quiero reservar una limpieza facial con Nadia Luisa."
- "Continuar con María Ignacia."
- "Agendame una hora sin pagar el abono."
- "Quiero comprar un producto para cuidar mi cabello."

## 22. Curl Validation Strategy

Curls minimos por PR:

- `GET /assistant/health`
- `POST /assistant/chat` con intencion de reserva.
- `POST /assistant/chat` con intento de evitar abono.
- `POST /assistant/chat` con producto.

Criterios:

- Health debe devolver `status: ok` y `module: assistant`.
- Booking debe responder sin crash.
- No-deposit debe mantener politica de abono 20%.
- Ninguna respuesta debe decir "reserva confirmada", "hora confirmada" o "cita agendada" antes de pago validado.

## 23. GitFlow Plan

Rama base:

- `develop`

Rama de trabajo:

- `feature/assistant-booking-conversion-flow`

Reglas:

- No usar squash.
- Mantener merge commits.
- Crear PRs pequenos por etapa.
- Ejecutar build, pytest assistant y curls antes de cada commit.
- No hacer push si el staging contiene archivos fuera del alcance.
- No eliminar la nueva rama hasta cerrar PR 8 o hasta instruccion explicita.

## 24. PR Roadmap

### PR 1 - Documentation and Contracts

Este PR actual.

- Documenta reglas comerciales, contratos y roadmap.

### PR 2 - Assistant State and Policies

- `services/api/app/assistant/state.py`
- `services/api/app/assistant/policies.py`
- `services/api/app/assistant/schemas.py`
- tests assistant
- No confirmar reservas reales.

### PR 3 - Professional Compatibility Rules

- Tools mock o service para validar profesional/servicio.
- Bloqueo cosmetología + Nadia Luisa.
- María Ignacia como profesional valida para cosmetología.

### PR 4 - Availability Read-Only Check

- Availability mock/read-only.
- Consultar disponibilidad sin reservar.
- No bloquear slot real todavia.

### PR 5 - Frontend Quick Replies

- Botones en el chat:
  - elegir profesional
  - elegir horario
  - continuar y pagar 20%
  - no por ahora
  - agregar producto al carrito

### PR 6 - Cart/Checkout Handoff

- Crear payload de carrito/checkout.
- Estado `pending_deposit`.
- Redireccion controlada.

### PR 7 - Notification Contract

- Email + WhatsApp + SMS fallback.
- No integracion real.
- Solo contrato y mocks.

### PR 8 - Tests, Curls and Documentation Closure

- pytest assistant
- curls booking/product/no-deposit
- build frontend
- rutas publicas
- cierre documental

## 25. Acceptance Criteria

Acceptance criteria para esta rama completa:

- El assistant detecta intencion de reserva como `booking_conversion`.
- El flujo solicita servicio si falta.
- El flujo solicita profesional si falta.
- El flujo bloquea cosmetología + Nadia Luisa.
- El flujo permite María Ignacia para cosmetología.
- El flujo solicita hora cuando solo hay dia.
- La disponibilidad es read-only hasta pago validado.
- Toda reserva de servicio exige abono 20%.
- El flujo prepara handoff a `/cart` o `/checkout`.
- El contrato incluye `cart_payload`, `quick_replies`, `redirect_target` y `safety`.
- No se crean reservas reales antes de pago validado.
- No se integran pagos reales.
- No se envia WhatsApp real.
- No se envia SMS real.
- Build frontend pasa.
- Tests assistant pasan.
- Curls minimos pasan.

## 26. Module Progress Impact

Impacto esperado por modulo:

- Modulo 6 - Notifications: sube en claridad contractual, no en integracion real.
- Modulo 7 - Booking Engine: gana ruta de conversion futura, sin cambiar reserva productiva.
- Modulo 8 - Schedule Engine: queda definido como fuente read-only futura.
- Modulo 10 - Cart + Checkout: gana contrato de handoff para abono.
- Modulo 13 - Storefront Experience: queda preparado para quick replies y redireccion.
- Modulo 14 - Recommendation + Assistant Intelligence Layer: pasa de assistant basico a roadmap de conversion comercial deterministica.
- Modulo 4 - Payments Core: queda como dependencia futura, sin avance de integracion.

## 27. Next Implementation Steps

Siguiente paso recomendado:

PR 2 - Assistant State and Policies.

Objetivo de PR 2:

- Agregar `booking_conversion`.
- Agregar `flow_step`.
- Definir schemas incrementales.
- Centralizar reglas comerciales en policies.
- Mantener compatibilidad con el widget actual.
- Validar que no se confirme ninguna reserva real.
