# Roadmap de Integraciones API — Always Beautiful

## 1. Propósito del documento

Este documento define el roadmap técnico para integrar APIs externas dentro del proyecto Always Beautiful Operations Platform.

Su objetivo es evitar integraciones improvisadas, proteger credenciales, separar sandbox de producción y mantener una arquitectura desacoplada.

Las integraciones externas deben tratarse como módulos de infraestructura de negocio, no como simples llamadas HTTP aisladas.

---

## 2. Principio central de integración

Toda API externa debe seguir este orden:

1. Documentación.
2. Sandbox.
3. Variables en `.env.example`.
4. Adaptador interno.
5. Tests.
6. Webhook si corresponde.
7. Pull Request independiente.
8. Producción solo con aprobación.

Codex no debe integrar APIs reales sin una rama específica y sin aprobación humana.

---

## 3. Diferencia con documentación previa

Antes de esta fase, el proyecto ya tenía módulos backend de pagos, envíos, órdenes y notificaciones.

Este documento no implementa esas APIs. Este documento define el orden correcto para integrarlas sin romper arquitectura, sin subir secretos y sin acoplar proveedores externos directamente al dominio del negocio.

---

## 4. APIs previstas

APIs o servicios previstos:

- Mercado Pago.
- PayPal.
- WhatsApp Business / Meta.
- Canva Connect API.
- Servicios de email.
- Servicios de webhooks.
- AWS.
- Proveedores logísticos futuros.

---

## 5. Mercado Pago

### Objetivo

Integrar pagos online para mercado local, especialmente Chile y Latinoamérica.

### Posible uso en Always Beautiful

- Pagos de productos.
- Abonos de reservas.
- Pagos completos de servicios seleccionados.
- Confirmación de checkout.
- Webhooks de estado de pago.

### Estado

Pendiente.

### Rama futura sugerida

```text
feature/payments-mercadopago-sandbox
```

### Reglas

- Usar sandbox.
- No usar credenciales productivas.
- No pegar tokens en código.
- Actualizar `.env.example`.
- Crear adaptador interno.
- Crear endpoints de webhook.
- Relacionar pago con Orders.
- Documentar flujo.

### Variables futuras posibles

```text
MERCADOPAGO_ACCESS_TOKEN=
MERCADOPAGO_PUBLIC_KEY=
MERCADOPAGO_WEBHOOK_SECRET=
MERCADOPAGO_ENVIRONMENT=sandbox
```

### Archivos candidatos

```text
services/api/app/payments/
services/api/app/orders/
services/api/app/notifications/
services/api/.env.example
docs/integrations/
```

### Validaciones futuras

- Crear preferencia de pago en sandbox.
- Recibir webhook de prueba.
- Actualizar estado de orden.
- Notificar evento.
- No generar pagos reales.

---

## 6. PayPal

### Objetivo

Integrar pagos internacionales o alternativa de pago online.

### Posible uso en Always Beautiful

- Pagos con cuenta PayPal.
- Pagos internacionales.
- Alternativa futura para tarjetas internacionales según estrategia comercial.

### Estado

Pendiente.

### Rama futura sugerida

```text
feature/payments-paypal-sandbox
```

### Reglas

- Usar sandbox.
- No usar client secret productivo.
- No subir credenciales.
- Crear adaptador independiente.
- No acoplar PayPal directamente al router principal.
- Documentar diferencias con Mercado Pago.

### Variables futuras posibles

```text
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_WEBHOOK_ID=
PAYPAL_ENVIRONMENT=sandbox
```

### Archivos candidatos

```text
services/api/app/payments/
services/api/app/orders/
services/api/.env.example
docs/integrations/
```

### Validaciones futuras

- Crear orden PayPal sandbox.
- Capturar pago sandbox.
- Recibir webhook sandbox.
- Actualizar Orders.
- Notificar evento.

---

## 7. Abstracción de proveedores de pago

Antes de integrar Mercado Pago o PayPal productivamente, debe crearse una capa de abstracción.

### Objetivo

Evitar que el dominio Orders dependa directamente de un proveedor específico.

### Rama futura sugerida

```text
feature/payments-provider-abstraction
```

### Diseño esperado

```text
payments/
├── client.py
├── routes.py
├── schemas.py
├── providers/
│   ├── base.py
│   ├── mercadopago.py
│   └── paypal.py
└── service.py
```

### Beneficio

- Permite cambiar proveedor sin romper Orders.
- Facilita tests.
- Permite sandbox por proveedor.
- Mantiene arquitectura empresarial.
- Evita lógica duplicada.

---

## 8. Webhooks

### Objetivo

Recibir eventos externos de pagos, notificaciones, logística o WhatsApp.

### Estado

Parcial en payments y notifications.

### Reglas

- Validar firma cuando el proveedor lo permita.
- No confiar en payloads sin validación.
- Registrar evento.
- Evitar duplicidad.
- Actualizar estado interno.
- Responder códigos HTTP correctos.
- No exponer secretos.

### Rama futura sugerida

```text
feature/webhooks-foundation
```

### Archivos candidatos

```text
services/api/app/payments/routes.py
services/api/app/notifications/routes.py
services/api/app/orders/service.py
services/api/app/core/config.py
```

---

## 9. Orders como centro de negocio

Orders debe actuar como centro de relación entre:

- Cart.
- Checkout.
- Payments.
- Shipping.
- Notifications.
- Storefront.

No se debe permitir que el Storefront hable directamente con proveedores externos.

Flujo ideal:

```text
Storefront → Backend Checkout → Orders → Payments Provider → Webhook → Orders → Notifications
```

---

## 10. Notifications

### Objetivo

Enviar o preparar notificaciones relacionadas con eventos del negocio.

Eventos futuros:

- Reserva creada.
- Reserva cancelada.
- Pago iniciado.
- Pago aprobado.
- Pago rechazado.
- Orden creada.
- Orden enviada.
- Postventa.
- Recomendación de producto.

### Reglas

- Separar evento de canal.
- No enviar notificaciones reales en pruebas sin confirmación.
- Usar plantillas.
- Documentar tono de marca.
- No mezclar notificaciones transaccionales con marketing sin política clara.

---

## 11. WhatsApp Business / Meta

### Objetivo futuro

Integrar comunicación con clientas mediante WhatsApp o mensajería empresarial.

### Estado

Futuro.

### Rama futura sugerida

```text
feature/messaging-whatsapp-foundation
```

### Reglas

- No integrar WhatsApp real sin cuenta, permisos y configuración.
- No enviar mensajes reales en pruebas.
- Documentar plantillas.
- Separar WhatsApp de IA.
- Separar WhatsApp de notificaciones transaccionales.
- Registrar eventos entrantes y salientes.
- Diseñar límites humanos antes de automatizar.

---

## 12. Canva Connect API

### Objetivo futuro

Automatizar o apoyar producción de campañas, piezas visuales y contenido.

### Estado

Futuro.

### Rama futura sugerida

```text
feature/marketing-canva-integration
```

### Reglas

- Mantener Canva manual primero.
- Documentar sistema de campañas.
- No asumir acceso API hasta validación.
- No conectar cuentas sin permisos.
- No automatizar publicaciones sin aprobación.
- Separar marketing manual de integración API.

---

## 13. AWS

### Objetivo futuro

Alojar servicios productivos y cargas pesadas fuera del MacBook Air 2017.

Componentes futuros:

- EC2 o ECS.
- RDS.
- Secrets Manager.
- CloudWatch.
- S3 si aplica.
- Docker en nube.
- CI/CD.

### Rama futura sugerida

```text
feature/aws-deployment-foundation
```

### Reglas

- Documentar arquitectura antes de crear recursos.
- Estimar costos.
- Usar IAM mínimo.
- Separar desarrollo de producción.
- No exponer puertos innecesarios.
- No desplegar sin rollback.
- No crear infraestructura real sin aprobación.

---

## 14. Política de `.env.example`

Toda integración externa debe actualizar `.env.example`, nunca archivos `.env` reales.

Ejemplo:

```text
PROVIDER_ENVIRONMENT=sandbox
PROVIDER_API_KEY=
PROVIDER_WEBHOOK_SECRET=
```

---

## 15. Política de tests

Toda integración debe incluir pruebas cuando aplique:

- Test de schema.
- Test de service.
- Test de webhook.
- Test de error.
- Test de idempotencia si aplica.
- Test de proveedor mock.
- Test de estado de orden si afecta Orders.

---

## 16. Orden recomendado de integraciones

Orden profesional recomendado:

1. Payments provider abstraction.
2. Mercado Pago sandbox.
3. PayPal sandbox.
4. Webhooks foundation.
5. Orders/payment state sync.
6. Notifications templates.
7. Checkout public integration.
8. WhatsApp foundation.
9. Canva documentation.
10. AWS deployment foundation.

---

## 17. Riesgos

Riesgos principales:

- Usar credenciales productivas en desarrollo.
- Subir tokens al repositorio.
- Acoplar Orders a un proveedor específico.
- No validar webhooks.
- Duplicar pagos por falta de idempotencia.
- Mezclar checkout, pagos y UI en un solo PR.
- Activar notificaciones reales por error.
- Crear costos AWS inesperados.
- Mezclar sandbox y producción.
- Permitir que frontend controle estados críticos de pago.

---

## 18. Regla final

Codex puede ayudar a diseñar integraciones, pero no debe activar servicios reales, usar credenciales productivas ni ejecutar operaciones externas sin autorización explícita.