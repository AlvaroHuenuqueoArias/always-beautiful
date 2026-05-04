# Roadmap de IA, LangChain y LangGraph — Always Beautiful

## 1. Propósito del documento

Este documento define el roadmap técnico para incorporar IA conversacional, memoria, recomendaciones y automatización inteligente dentro del proyecto Always Beautiful Operations Platform.

El objetivo es evitar una implementación prematura o desordenada de IA. La IA debe integrarse de forma progresiva, controlada, validable y conectada con datos reales del negocio.

---

## 2. Principio central

Always Beautiful no debe iniciar con Machine Learning real ni agentes complejos sin datos reales.

La estrategia correcta es:

1. Reglas determinísticas.
2. Asistente básico.
3. Memoria corta.
4. Catálogo consultable.
5. LangChain o LangGraph cuando exista caso real.
6. Memoria persistente.
7. WhatsApp real.
8. Recomendaciones más avanzadas.

---

## 3. Diferencia con documentación previa

Antes de esta fase, el proyecto tenía una idea futura de asistente, botón flotante y recomendaciones.

Este documento convierte esa intención en roadmap técnico. Su función es evitar que Codex implemente una IA completa antes de tener catálogo real, datos reales, políticas, backend estable y reglas de negocio verificables.

---

## 4. Alcance futuro de IA

La capa de IA podrá apoyar:

- Atención conversacional.
- Recomendaciones de productos.
- Recomendaciones post-servicio.
- Cross-sell.
- Bundles.
- Consulta de servicios.
- Orientación de reservas.
- Respuestas frecuentes.
- Automatización de postventa.
- Asistencia interna para la dueña.
- Apoyo al Dashboard administrativo.

---

## 5. Lo que NO debe hacer la IA

La IA no debe:

- Diagnosticar condiciones médicas.
- Prometer resultados cosméticos garantizados.
- Inventar fuentes.
- Inventar precios reales.
- Inventar disponibilidad.
- Confirmar reservas sin motor backend.
- Confirmar pagos sin proveedor.
- Usar datos personales sin control.
- Exponer información interna.
- Enviar mensajes reales sin aprobación.
- Reemplazar revisión humana en decisiones sensibles.

---

## 6. Fase 1 — Reglas determinísticas

### Objetivo

Crear recomendaciones simples basadas en reglas controladas.

Ejemplo:

```text
Si la clienta selecciona tratamiento capilar X, sugerir producto Y como complemento.
```

### Beneficio

- No requiere modelo ML.
- Es auditable.
- Es fácil de explicar.
- Reduce riesgo.
- Funciona antes de tener datos masivos.
- Puede validarse con datos de negocio simples.

### Rama futura sugerida

```text
feature/recommendations-rule-based
```

### Archivos candidatos

```text
services/api/app/recommendations/
web/src/pages/public/ProductsPage.jsx
web/src/pages/public/CheckoutPage.jsx
docs/ai/
```

---

## 7. Fase 2 — Assistant endpoint básico

### Objetivo

Crear un endpoint backend para asistente controlado.

No debe ser todavía WhatsApp real.

### Rama futura sugerida

```text
feature/assistant-endpoint-foundation
```

### Responsabilidades

- Recibir pregunta.
- Identificar intención.
- Responder con reglas o conocimiento controlado.
- No inventar información.
- No acceder a secretos.
- No ejecutar acciones reales.
- Registrar límites funcionales.

### Archivos candidatos

```text
services/api/app/assistant/
services/api/app/catalog/
services/api/app/booking/
docs/ai/
```

---

## 8. Fase 3 — Memoria corta

### Objetivo

Permitir continuidad dentro de una sesión.

Ejemplo:

- Servicio consultado.
- Producto visto.
- Preferencia de horario.
- Preferencia de profesional.

### Riesgo

No almacenar datos sensibles sin política clara.

### Rama futura sugerida

```text
feature/assistant-session-memory
```

### Regla

Memoria corta significa memoria temporal de sesión, no historial permanente de clientas.

---

## 9. Fase 4 — Catálogo consultable

### Objetivo

Permitir que el asistente consulte servicios y productos desde una fuente estructurada.

### Requisitos

- Catálogo ordenado.
- Servicios reales.
- Productos reales.
- Precios definidos.
- Descripciones revisadas.
- Relación producto-servicio.

### Regla

No usar respuestas inventadas. El asistente debe responder desde datos controlados.

---

## 10. Fase 5 — LangChain

### Objetivo

Evaluar LangChain como capa de orquestación para herramientas, prompts y recuperación de contexto.

### Uso potencial

- Consulta de catálogo.
- Consulta de servicios.
- FAQ.
- Resumen de políticas.
- Recomendaciones asistidas.
- Apoyo a la dueña en consultas internas.

### Regla

No integrar LangChain hasta tener caso de uso específico.

### Rama futura sugerida

```text
feature/ai-langchain-foundation
```

---

## 11. Fase 6 — LangGraph

### Objetivo

Evaluar LangGraph para flujos conversacionales con estados.

### Uso potencial

- Flujo de reserva guiada.
- Flujo de recomendación.
- Flujo de postventa.
- Flujo de asistencia interna.
- Flujo de recuperación de carrito.

### Regla

No usar LangGraph para todo. Usarlo solo cuando exista flujo multiestado claro.

### Rama futura sugerida

```text
feature/ai-langgraph-conversation-flow
```

---

## 12. Fase 7 — Memoria persistente

### Objetivo

Guardar preferencias o contexto histórico con control.

### Requisitos

- Política de datos.
- Consentimiento si aplica.
- Base de datos.
- Separación por clienta.
- Seguridad.
- Eliminación o actualización de datos.
- Trazabilidad.

### Riesgo

Alto si se implementa sin política de privacidad.

---

## 13. Fase 8 — WhatsApp real

### Objetivo

Conectar el asistente o notificaciones a WhatsApp Business / Meta.

### Requisitos

- Cuenta empresarial.
- Permisos.
- Plantillas.
- Webhooks.
- Reglas de atención.
- Control humano.
- Logs.
- Separación entre mensajes transaccionales, marketing e IA.

### Regla

WhatsApp debe ir después de tener:

- Notificaciones.
- Assistant endpoint.
- Políticas.
- Webhooks.
- Mensajes aprobados.
- Datos reales.

---

## 14. Recomendaciones de productos

### Objetivo

Sugerir productos relacionados con servicios o tratamientos.

### Primera etapa

Reglas determinísticas.

Ejemplo:

```text
Servicio: hidratación capilar
Producto recomendado: shampoo o máscara de cuidado compatible
Motivo: complementar rutina posterior al servicio
```

### Interfaz esperada

La clienta debe poder:

- Agregar producto.
- Descartar producto.
- Ver explicación.
- Ver fuente o criterio.
- Continuar compra.

### Regla

No afirmar efectividad médica o garantizada. Usar lenguaje prudente, comercial y verificable.

---

## 15. Fuentes para recomendaciones

Las recomendaciones deben basarse en:

- Datos del salón.
- Relación servicio-producto.
- Información del fabricante.
- Fuentes confiables cuando corresponda.
- Experiencia profesional del negocio.

No inventar fuentes.

---

## 16. IA para Dashboard interno

La IA también puede apoyar el panel interno:

- Resumen de ventas.
- Alertas de baja demanda.
- Recomendaciones de stock.
- Servicios más rentables.
- Tendencias.
- Sugerencias de campañas.
- Lectura ejecutiva de métricas.

Esto debe hacerse en ramas del Dashboard, no mezclado con Storefront.

---

## 17. Orden recomendado de implementación

1. Documentar datos reales necesarios.
2. Crear recomendaciones rule-based.
3. Crear assistant endpoint básico.
4. Crear memoria de sesión.
5. Conectar catálogo.
6. Evaluar LangChain.
7. Evaluar LangGraph.
8. Crear UI conversacional.
9. Integrar WhatsApp.
10. Evaluar ML real si existen datos suficientes.

---

## 18. Riesgos

Riesgos principales:

- Implementar IA sin datos reales.
- Crear respuestas no verificables.
- Prometer resultados.
- Exponer datos de clientas.
- Mezclar asistente con pagos sin seguridad.
- Hacer recomendaciones médicas.
- Automatizar WhatsApp sin control.
- Crear dependencia innecesaria de LLM.
- Mezclar recomendaciones comerciales con afirmaciones no verificadas.

---

## 19. Regla final

La IA debe aumentar la calidad operativa y comercial del salón, no reemplazar reglas de negocio, validaciones backend ni supervisión humana.