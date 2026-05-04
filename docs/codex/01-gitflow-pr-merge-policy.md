# Política GitFlow, Pull Requests y Merge Commits — Always Beautiful

## 1. Propósito del documento

Este documento define la política oficial de ramas, commits, Pull Requests y merge commits para el proyecto Always Beautiful.

El objetivo es proteger el historial del repositorio, mantener trazabilidad profesional y evitar integraciones desordenadas.

---

## 2. Modelo de ramas

El proyecto utiliza un flujo basado en GitFlow adaptado al desarrollo modular.

### Ramas principales

- `main`: rama estable.
- `develop`: rama de integración.
- `feature/*`: nuevas funcionalidades.
- `fix/*`: correcciones.
- `release/*`: preparación de versiones.

---

## 3. Regla de rama base

Toda rama `feature/*` debe nacer desde `develop`.

Flujo recomendado:

~~~bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-del-modulo
~~~

No se debe crear una feature branch desde `main` salvo autorización explícita.

---

## 4. Restricción del comando `git switch`

En este proyecto se debe usar:

~~~bash
git checkout nombre-rama
~~~

No se debe usar:

~~~bash
git switch nombre-rama
~~~

Motivo: el entorno local del proyecto y el flujo histórico del usuario se han construido usando `git checkout`.

---

## 5. Convención de commits

Los commits deben escribirse en español formal, usando estructura tipo Conventional Commits.

Formato:

~~~text
tipo(scope): descripción breve
~~~

Tipos permitidos:

- `feat`: nueva funcionalidad.
- `fix`: corrección.
- `style`: cambios visuales o de formato.
- `refactor`: reorganización sin cambio funcional externo.
- `docs`: documentación.
- `test`: pruebas.
- `build`: dependencias, tooling o sistema de build.
- `chore`: mantenimiento general.

Ejemplos:

~~~text
feat(storefront): estructurar footer institucional y páginas legales iniciales
style(storefront): adaptar experiencia pública a móvil y tablet
docs(codex): documentar modelo operativo para agentes de desarrollo
docs(architecture): registrar estado modular de la plataforma
test(api): validar rutas protegidas del backend
~~~

---

## 6. Separación de commits

No se deben crear commits gigantes que mezclen cambios no relacionados.

Ejemplo incorrecto:

~~~text
feat(project): update everything
~~~

Ejemplo correcto:

~~~text
docs(codex): establecer reglas operativas para agentes
docs(codex): documentar política GitFlow y Pull Requests
docs(architecture): registrar estado modular de la plataforma
docs(integrations): definir roadmap de APIs externas
~~~

---

## 7. Regla antes de commit

Antes de cualquier commit se debe ejecutar:

~~~bash
git status --short
~~~

Cuando aplique, también:

~~~bash
git diff --stat
~~~

El objetivo es confirmar qué archivos entrarán al commit.

---

## 8. Regla de `git add`

Los `git add` deben ser explícitos y por archivo o bloque coherente.

Ejemplo:

~~~bash
git add AGENTS.md .github/pull_request_template.md
~~~

Ejemplo:

~~~bash
git add docs/codex/00-operating-model.md docs/codex/01-gitflow-pr-merge-policy.md docs/codex/02-task-prompt-templates.md docs/codex/03-feedback-protocol.md docs/codex/project-context-audit.md
~~~

No se recomienda usar:

~~~bash
git add .
~~~

salvo que se haya validado cuidadosamente el estado completo del repositorio.

---

## 9. Regla después de commit

Después de cualquier commit se debe ejecutar:

~~~bash
git log --oneline --graph --decorate -10
~~~

Esto permite verificar que el historial mantiene coherencia.

---

## 10. Política de push

No se debe ejecutar push sin autorización explícita.

Cuando se autorice:

~~~bash
git push origin nombre-rama
~~~

Ejemplo:

~~~bash
git push origin feature/codex-operating-model
~~~

---

## 11. Política de Pull Requests

Todo Pull Request debe tener:

1. Resumen.
2. Alcance incluido.
3. Alcance excluido.
4. Módulo afectado.
5. Tipo de cambio.
6. Validaciones ejecutadas.
7. Riesgos revisados.
8. Decisiones técnicas.
9. Nota de alcance.
10. Checklist final.

La plantilla oficial se encuentra en:

~~~text
.github/pull_request_template.md
~~~

---

## 12. Crear PR con GitHub CLI

Cuando la rama esté lista y el push autorizado, se puede crear PR con:

~~~bash
gh pr create --base develop --head nombre-rama --title "título formal" --body "descripción formal"
~~~

Ejemplo:

~~~bash
gh pr create --base develop --head feature/codex-operating-model --title "docs(codex): establecer modelo operativo para agentes" --body "Este PR integra la documentación base para operar Codex CLI, Codex App y agentes técnicos dentro del proyecto Always Beautiful."
~~~

---

## 13. Política de merge commit

No se debe hacer squash.

Cuando el PR esté revisado y aprobado, se debe fusionar con merge commit:

~~~bash
gh pr merge --merge
~~~

No se debe eliminar la rama automáticamente salvo autorización explícita.

---

## 14. Política de ramas activas

No eliminar ramas hasta que el usuario lo autorice.

Antes de eliminar una rama, confirmar:

- PR fusionado.
- `develop` actualizado.
- No quedan cambios locales.
- No hay trabajo pendiente en la rama.
- El usuario aprobó eliminación.

---

## 15. Política de `stash`

El uso de `git stash` es válido para preservar trabajo local antes de cambiar de rama.

Ejemplo usado en el proyecto:

~~~bash
git stash push -u -m "wip(storefront): preservar avance local de home services antes de configurar codex"
~~~

Antes de aplicar un stash se debe ejecutar:

~~~bash
git stash list
git status --short
~~~

Aplicar stash solo con autorización:

~~~bash
git stash apply stash@{0}
~~~

No eliminar stash hasta confirmar que el trabajo fue recuperado correctamente.

---

## 16. Política para `feature/storefront-home-services`

La rama `feature/storefront-home-services` contiene trabajo local preservado en stash.

No aplicar el stash dentro de `feature/codex-operating-model`.

La rama `feature/codex-operating-model` debe enfocarse únicamente en documentación, reglas de operación, PR template y contexto técnico para Codex.

---

## 17. Criterio de cierre de una feature branch

Una rama puede prepararse para PR cuando:

- El alcance está claro.
- Los archivos corresponden al módulo.
- No hay archivos basura.
- Las validaciones aplicables pasaron.
- Los commits están separados.
- El PR explica qué incluye y qué excluye.
- No hay secretos.
- No se modificó `main`.

---

## 18. Regla final

El historial Git es parte de la calidad técnica del proyecto.

Un buen historial debe permitir entender:

- Qué se hizo.
- Por qué se hizo.
- En qué módulo ocurrió.
- Qué quedó fuera.
- Qué validaciones se ejecutaron.
