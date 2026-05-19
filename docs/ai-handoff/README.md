# Sistema de handoff de IA — Always Beautiful

Esta carpeta coordina el trabajo entre Codex CLI y DeepSeek vía OpenCode.

El objetivo es mantener a las IA alineadas, auditables y sincronizadas.

## Agentes operativos actuales

1. Codex CLI / OpenAI Plus  
   Rol: Principal Fullstack Software Engineer.

2. DeepSeek V4 Flash vía OpenCode  
   Rol: Backend Developer / Backend Debugging Assistant.

3. DeepSeek V4 Pro vía OpenCode  
   Rol: Frontend Advanced / Architecture Reviewer.

## Agente pausado

Gemini 3 Flash Preview vía OpenCode + OpenRouter queda pausado.

Motivo:

- OpenRouter devolvió error de créditos/max_tokens.
- El flujo gratuito no es estable para diagnósticos largos.
- El proyecto no debe depender de OpenRouter hasta que existan créditos o límites confiables.

## Regla central

Una sola IA puede modificar archivos por turno.

Todas las IA deben leer contexto antes de actuar.

Todas las IA deben actualizar el handoff después de actuar.

Codex CLI conserva la autoridad técnica principal.

## Archivos obligatorios de lectura

Ningún agente debe trabajar sin leer:

- `AGENTS.md`
- `docs/ai-handoff/ACTIVE_CONTEXT.md`
- `docs/ai-handoff/AGENT_ROLES.md`
- `docs/ai-handoff/CHANGELOG_AI.md`

Si trabaja backend, debe leer también:

- `docs/ai-handoff/BACKEND_HANDOFF.md`

Si trabaja frontend, debe leer también:

- `docs/ai-handoff/FRONTEND_HANDOFF.md`

Si Codex CLI debe retomar el trabajo, debe leer también:

- `docs/ai-handoff/CODEX_REENTRY.md`