# Modelo Operativo de Codex — Always Beautiful

## 1. Propósito del documento

Este documento define cómo debe utilizarse Codex CLI, Codex App y cualquier agente de asistencia técnica dentro del proyecto Always Beautiful.

El objetivo es establecer una forma de trabajo segura, ordenada, auditable y compatible con GitFlow, evitando que los agentes modifiquen archivos sensibles, mezclen módulos o ejecuten acciones destructivas sin autorización.

Codex debe entender que el proyecto no es un prototipo aislado, sino una plataforma fullstack modular para operar profesionalmente un salón de belleza.

---

## 2. Principio operativo central

La regla principal del proyecto es:

> Codex no mejora libremente. Codex ejecuta cambios autorizados, en archivos autorizados, con validación obligatoria y feedback técnico.

Esto significa que Codex debe trabajar bajo estas condiciones:

1. Alcance definido.
2. Archivos permitidos.
3. Archivos prohibidos.
4. Validaciones requeridas.
5. Criterio de cierre.
6. Revisión humana antes de commit, push, Pull Request o merge.

---

## 3. Responsabilidad del usuario

El usuario mantiene la dirección técnica del proyecto.

El usuario define:

- Qué módulo se trabaja.
- Qué rama se usa.
- Qué archivos pueden modificarse.
- Qué archivos quedan prohibidos.
- Qué validaciones deben ejecutarse.
- Cuándo se permite hacer commit.
- Cuándo se permite hacer push.
- Cuándo se permite crear Pull Request.
- Cuándo se permite hacer merge commit.

Codex no debe tomar estas decisiones de forma autónoma.

---

## 4. Responsabilidad de Codex

Codex puede actuar como ejecutor técnico controlado.

Codex puede:

- Auditar el estado del repositorio.
- Leer archivos autorizados.
- Proponer cambios.
- Implementar cambios acotados.
- Ejecutar build o tests cuando esté autorizado.
- Preparar mensajes de commit.
- Preparar descripción de Pull Request.
- Documentar decisiones técnicas.
- Detectar riesgos.
- Sugerir separación de commits.

Codex no puede:

- Crear ramas sin autorización.
- Hacer push sin autorización.
- Hacer merge sin autorización.
- Modificar archivos sensibles sin explicar el impacto.
- Integrar APIs reales sin sandbox y aprobación.
- Instalar dependencias sin justificarlo.
- Reescribir componentes completos sin permiso.
- Cambiar diseño aprobado sin autorización.
- Inventar datos reales.
- Manipular secretos o credenciales.

---

## 5. Modo recomendado de ejecución local

Cuando se use Codex CLI, debe abrirse desde la raíz del repositorio:

~~~bash
cd ~/Dev/always-beautiful
codex --sandbox workspace-write --ask-for-approval on-request
~~~

Este modo permite que Codex trabaje dentro del proyecto, pero mantiene control humano sobre acciones sensibles.

No se debe ejecutar Codex desde carpetas internas como:

~~~text
web/
services/api/
docs/
~~~

El agente debe ver la estructura completa del repositorio para razonar correctamente.

---

## 6. Flujo mínimo antes de cualquier tarea

Antes de modificar archivos, Codex debe revisar:

~~~bash
git rev-parse --abbrev-ref HEAD
git status --short
git log --oneline --graph --decorate -10
~~~

Luego debe informar:

1. Rama actual.
2. Archivos modificados.
3. Archivos nuevos.
4. Archivos sensibles detectados.
5. Riesgos.
6. Archivos que propone tocar.
7. Archivos que no tocará.
8. Comandos que ejecutará.

Si el usuario no aprueba, Codex no modifica archivos.

---

## 7. Flujo estándar de una tarea

Cada tarea debe seguir este ciclo:

1. Diagnóstico de entrada.
2. Confirmación de alcance.
3. Propuesta técnica.
4. Aprobación del usuario.
5. Modificación acotada.
6. Validación.
7. Informe de salida.
8. Recomendación de commit.
9. Revisión humana.
10. Commit autorizado.
11. Push autorizado.
12. Pull Request autorizado.
13. Merge commit autorizado.

---

## 8. Regla de módulo único

Cada tarea debe afectar un módulo principal.

Ejemplos de módulos:

- Storefront Experience.
- Admin Panel Frontend.
- Admin Panel Backend.
- Auth / Security.
- Observability.
- Catalog.
- Cart / Checkout.
- Orders.
- Payments.
- Shipping.
- Booking.
- Schedule.
- Notifications.
- Documentation.
- DevOps / Tooling.
- Integrations.
- Marketing / Canva.
- Assistant Intelligence.

No se deben mezclar módulos sin justificación explícita.

---

## 9. Regla de archivos sensibles

Los siguientes archivos requieren especial cuidado:

- `web/src/index.css`
- `web/src/design/tokens.js`
- `web/src/App.jsx`
- `web/src/main.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/layouts/AdminLayout.jsx`
- `web/src/layouts/PublicLayout.jsx`
- `web/package.json`
- `web/package-lock.json`
- `services/api/requirements.txt`
- `services/api/app/main.py`
- `services/api/app/core/config.py`
- `services/api/app/auth/security.py`
- `.env.example`
- `services/api/.env.example`

Si Codex necesita modificar alguno, debe explicar:

1. Por qué es necesario.
2. Qué riesgo tiene.
3. Qué módulo puede afectar.
4. Cómo se validará.
5. Qué alternativa existe sin tocar ese archivo.

---

## 10. Regla de documentación

Toda decisión técnica relevante debe quedar documentada en alguno de estos lugares:

- `README.md`
- `docs/`
- Pull Request description
- Commit message, cuando corresponda

La documentación debe mantener tono formal, profesional y técnico.

---

## 11. Validaciones por tipo de cambio

### Frontend

Para cambios en `web/`:

~~~bash
npm --prefix web run build
~~~

Además, si aplica Storefront:

- Revisar `/`.
- Revisar `/services`.
- Revisar `/products`.
- Revisar `/booking`.
- Revisar `/cart`.
- Revisar `/checkout`.
- Revisar `/admin`.

### Backend

Para cambios en `services/api/`:

~~~bash
cd services/api
source .venv/bin/activate
pytest
deactivate
cd ../..
~~~

### Documentación

Para cambios solo en documentación:

- Revisar formato Markdown.
- Revisar enlaces internos si existen.
- Revisar `git status --short`.
- No es obligatorio ejecutar build si no se toca código.

---

## 12. Política de instalación de dependencias

Codex no debe instalar dependencias sin autorización.

Antes de proponer una instalación debe indicar:

1. Nombre del paquete.
2. Motivo técnico.
3. Archivos afectados.
4. Riesgo.
5. Peso o impacto aproximado.
6. Alternativa sin instalar.
7. Validación posterior.

---

## 13. Política de APIs externas

Las APIs externas deben integrarse en ramas específicas.

Orden obligatorio:

1. Documentación.
2. Sandbox.
3. Variables en `.env.example`.
4. Adaptador interno.
5. Tests.
6. Webhooks si corresponde.
7. Pull Request independiente.
8. Producción solo con aprobación.

APIs futuras previstas:

- Mercado Pago.
- PayPal.
- Canva Connect API.
- WhatsApp Business / Meta.
- AWS.
- Servicios de email o notificaciones.

---

## 14. Política de IA

Las integraciones con IA deben avanzar de forma progresiva.

Orden recomendado:

1. Assistant endpoint básico.
2. Session ID.
3. Memoria corta.
4. Reglas determinísticas.
5. Catálogo consultable.
6. LangGraph.
7. Memoria persistente.
8. WhatsApp real.

No se debe iniciar con Machine Learning real sin datos reales suficientes.

---

## 15. Política de hardware local

El proyecto se desarrolla en un MacBook Air 2017 con limitaciones de rendimiento.

Por eso se debe evitar localmente:

- Docker pesado.
- Compilaciones innecesarias.
- Dependencias de gran tamaño sin justificación.
- Servicios concurrentes no requeridos.
- ML pesado.
- Instalaciones masivas mediante Homebrew.

El entorno local debe usarse para:

- React/Vite.
- FastAPI liviano.
- pytest.
- Codex CLI.
- Git.
- Build controlado.

AWS se usará más adelante para cargas productivas o más pesadas.

---

## 16. Criterio de éxito del modelo operativo

El modelo operativo se considera correctamente aplicado cuando:

- Codex diagnostica antes de modificar.
- El usuario aprueba el alcance.
- Los cambios son pequeños y revisables.
- Los commits están separados por categoría.
- El PR explica alcance incluido y excluido.
- El historial Git mantiene coherencia.
- No se suben secretos.
- No se mezclan módulos sin justificación.
- Las validaciones se ejecutan antes del cierre.

---

## 17. Regla final

Ante cualquier duda, Codex debe detenerse y pedir autorización.

Es preferible avanzar más lento con control técnico que romper una base estable por exceso de automatización.
