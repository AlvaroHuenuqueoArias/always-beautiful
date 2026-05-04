# Protocolo de Feedback para Codex — Always Beautiful

## 1. Propósito del documento

Este documento define cómo debe entregar feedback Codex antes, durante y después de trabajar en el proyecto Always Beautiful.

El objetivo es evitar cambios invisibles, decisiones no documentadas, modificaciones fuera de alcance y commits poco auditables.

---

## 2. Principio central

Codex debe trabajar con feedback técnico permanente.

Cada intervención debe responder:

- Qué encontró.
- Qué hará.
- Qué no hará.
- Qué modificó.
- Qué validó.
- Qué riesgo queda.
- Qué recomienda después.

---

## 3. Feedback de entrada obligatorio

Antes de modificar cualquier archivo, Codex debe entregar:

1. Rama actual.
2. Estado de Git.
3. Archivos modificados.
4. Archivos nuevos.
5. Archivos sensibles detectados.
6. Objetivo interpretado.
7. Alcance permitido.
8. Alcance excluido.
9. Archivos que tocará.
10. Archivos que no tocará.
11. Comandos que ejecutará.
12. Riesgos iniciales.

---

## 4. Formato de feedback de entrada

~~~text
Diagnóstico de entrada

Rama actual:
- [rama]

Estado Git:
- [resumen]

Archivos modificados:
- [lista]

Archivos nuevos:
- [lista]

Archivos sensibles:
- [lista]

Objetivo interpretado:
- [objetivo]

Alcance permitido:
- [lista]

Alcance excluido:
- [lista]

Archivos que tocaré:
- [lista]

Archivos que no tocaré:
- [lista]

Comandos que ejecutaré:
- [lista]

Riesgos:
- [lista]

Necesito autorización antes de modificar.
~~~

---

## 5. Feedback durante la tarea

Si Codex detecta un problema durante la ejecución, debe detenerse y explicar:

- Qué encontró.
- Por qué afecta el alcance.
- Qué alternativas existen.
- Qué recomienda.
- Qué autorización necesita.

No debe resolver automáticamente si la solución implica tocar archivos fuera del alcance.

---

## 6. Feedback de salida obligatorio

Después de modificar archivos, Codex debe entregar:

1. Archivos modificados.
2. Archivos creados.
3. Archivos no tocados.
4. Cambios realizados.
5. Comandos ejecutados.
6. Resultado de build/tests.
7. Riesgos pendientes.
8. Validaciones pendientes.
9. Siguiente paso recomendado.
10. Commit sugerido.
11. Pull Request sugerido si aplica.

---

## 7. Formato de feedback de salida

~~~text
Informe de salida

Archivos modificados:
- [lista]

Archivos creados:
- [lista]

Archivos no tocados:
- [lista]

Cambios realizados:
- [lista]

Comandos ejecutados:
- [lista]

Resultado de validaciones:
- [resultado]

Riesgos pendientes:
- [lista]

Validaciones pendientes:
- [lista]

Siguiente paso recomendado:
- [paso]

Commit sugerido:
- [mensaje]

Pull Request sugerido:
- [título y resumen si aplica]
~~~

---

## 8. Feedback para documentación

Cuando la tarea sea solo documentación, Codex debe indicar:

- Archivos documentales actualizados.
- Si se tocó código o no.
- Si se requiere build o no.
- Si hay impacto operativo.
- Commit sugerido.

Ejemplo:

~~~text
Esta tarea solo modifica documentación.
No se modificó código.
No se requiere build frontend.
No se requiere pytest backend.
Commit sugerido:
docs(codex): documentar protocolo de feedback para agentes
~~~

---

## 9. Feedback para frontend

Cuando la tarea toque frontend, Codex debe indicar:

- Rutas afectadas.
- Componentes afectados.
- CSS global afectado.
- Riesgo sobre `/admin`.
- Validación `npm --prefix web run build`.
- Validación visual requerida.

Debe advertir especialmente si toca:

- `web/src/index.css`
- `web/src/design/tokens.js`
- `web/src/App.jsx`
- `web/src/app/AppRouter.jsx`
- `web/src/layouts/*`
- `web/src/components/shared/*`

---

## 10. Feedback para backend

Cuando la tarea toque backend, Codex debe indicar:

- Módulo afectado.
- Router afectado.
- Schema afectado.
- Service afectado.
- Repository afectado.
- Tests afectados.
- Variables de entorno afectadas.
- Resultado de pytest.

Debe advertir especialmente si toca:

- `services/api/app/main.py`
- `services/api/app/core/config.py`
- `services/api/app/db/*`
- `services/api/app/auth/*`
- `services/api/requirements.txt`

---

## 11. Feedback para APIs externas

Cuando la tarea implique APIs externas, Codex debe indicar:

- API objetivo.
- Modo sandbox o producción.
- Variables necesarias.
- Archivos `.env.example` afectados.
- Riesgo de secretos.
- Webhooks necesarios.
- Tests necesarios.
- Documentación necesaria.

Nunca debe pedir ni imprimir tokens reales en la conversación o en archivos versionados.

---

## 12. Feedback para IA

Cuando la tarea implique IA, Codex debe indicar:

- Tipo de IA.
- Si es rule-based, LLM o ML.
- Datos requeridos.
- Riesgo de alucinación.
- Riesgo de recomendaciones no verificadas.
- Límite funcional.
- Fuente o criterio para recomendaciones.

---

## 13. Feedback para Git

Antes de recomendar commit, Codex debe solicitar o ejecutar:

~~~bash
git status --short
git diff --stat
~~~

Después de commit, debe solicitar o ejecutar:

~~~bash
git log --oneline --graph --decorate -10
~~~

No debe hacer push sin autorización.

---

## 14. Feedback para Pull Request

Antes de crear un PR, Codex debe preparar:

- Título.
- Resumen.
- Alcance incluido.
- Alcance excluido.
- Módulo afectado.
- Validaciones.
- Riesgos.
- Nota de alcance.
- Checklist.

---

## 15. Regla final

Si Codex no puede explicar claramente qué hizo, por qué lo hizo y cómo se validó, el cambio no debe considerarse listo para commit.
